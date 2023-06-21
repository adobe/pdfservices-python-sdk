# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import json
import logging
import sys
from datetime import datetime, timedelta
from http import HTTPStatus

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.auth.session_token import SessionToken
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants, custom_error_messages
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest


class ServicePrincipalAuthenticator(Authenticator):
    """
        Authenticator for OAuth Server-to-Server based Service Principal credentials
    """
    token: SessionToken = None
    service_principal_configuration: ServicePrincipalCredentials
    token_endpoint = ''

    def __init__(self, service_principal_configuration, client_config):
        self.service_principal_configuration = service_principal_configuration
        self.token_endpoint = client_config.get_pdf_services_uri()
        self._logger = logging.getLogger(__name__)
        pass

    def session_token(self):
        """ Access token for the PDF Services API """
        if self.token:
            if self.older_in_minute() <= 2:
                return self.token
        return self.refresh_token()

    def older_in_minute(self):
        """ Time remaining in minutes till token expiry """
        return int((datetime.now() - self.token.expired_at).seconds / 60)

    def refresh_token(self):
        """ Refreshes the access token sent to PDF Services API """

        url = "{token_endpoint}/{ims_proxy_token_endpoint}".format(
            token_endpoint=self.token_endpoint,
            ims_proxy_token_endpoint='token'
        )
        access_token_request_payload = {"client_id": self.service_principal_configuration.client_id,
                                        "client_secret": self.service_principal_configuration.client_secret}

        try:
            http_request = HttpRequest(http_method=HttpMethod.POST, request_key=RequestKey.AUTHN, url=url,
                                       data=access_token_request_payload, headers={})
            response = http_client.process_request(http_request=http_request, success_status_codes=[HTTPStatus.OK],
                                                   error_response_handler=self.handle_ims_failure)

            content = json.loads(response.content)
            self.token = SessionToken(content['access_token'], content['expires_in'])
        except Exception:
            raise SdkException("Exception in fetching access token", sys.exc_info())
        return self.token

    def get_api_key(self):
        """ API key for Service Principle credentials """
        return self.service_principal_configuration.client_id

    def handle_ims_failure(self, response):
        """ Handling of IMS failure during call to PDF Services API """

        self._logger.error(
            "IMS call failed with status code {error_code}".format(error_code=response.status_code))
        content = json.loads(response.content)
        # When error is returned with no description
        if not content.get("error_description", None) or content["error_description"].isspace():
            content["error_description"] = content.get("error", None)
        # Special handling for invalid token and certificate expiry cases
        if "invalid_token"==content.get("error", None):
            if "Could not match signature to any of the bindings"==content.get("error_description",None):
                content["error_description"] = custom_error_messages["imsCertificateExpiredErrorMessage"]
            else:
                content["error_description"] = custom_error_messages["imsInvalidTokenGenericErrorMessage"]
        raise OperationException(message="Error response received for IMS request",
                                 status_code=response.status_code,
                                 error_code=content.get("error", None),
                                 error_message=content.get("error_description", None),
                                 request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, True))
