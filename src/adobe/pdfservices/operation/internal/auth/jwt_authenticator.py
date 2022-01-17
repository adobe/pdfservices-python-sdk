# Copyright 2021 Adobe. All rights reserved.
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

import jwt

from adobe.pdfservices.operation.auth.service_account_credentials import ServiceAccountCredentials
from adobe.pdfservices.operation.exception.exceptions import SdkException, ServiceApiException
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.auth.session_token import SessionToken
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants, custom_error_messages
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest


class JwtAuthenticator(Authenticator):
    token: SessionToken = None
    service_account_configuration: ServiceAccountCredentials
    jwt_endpoint = ''

    def __init__(self, service_account_configuration):
        self.service_account_configuration = service_account_configuration
        self._logger = logging.getLogger(__name__)
        pass

    def session_token(self):
        if self.token:
            if self.older_in_minute() <= 2:
                return self.token
        return self.refresh_token()

    def older_in_minute(self):
        return int((datetime.now() - self.token.expired_at).seconds / 60)

    def refresh_token(self):
        jwt_token = self._prepare_jwt()
        url = "{jwt_endpoint}/{jwt_uri_suffix}".format(
            jwt_endpoint=self.service_account_configuration.ims_base_uri,
            jwt_uri_suffix=ServiceConstants.JWT_URI_SUFFIX
        )
        access_token_request_payload = {"jwt_token": jwt_token,
                                        "client_id": self.service_account_configuration.client_id,
                                        "client_secret": self.service_account_configuration.client_secret}
        try:
            http_request = HttpRequest(http_method=HttpMethod.POST, url=url, data=access_token_request_payload,
                                       headers={})
            response = http_client.process_request(http_request=http_request, success_status_codes=[HTTPStatus.OK],
                                                   error_response_handler=self.handle_ims_failure)
            content = json.loads(response.content)
            self.token = SessionToken(content['access_token'], content['expires_in'])
        except Exception:
            raise SdkException("Exception in fetching access token", sys.exc_info())
        return self.token

    def get_api_key(self):
        return self.service_account_configuration.client_id

    def handle_ims_failure(self, response):
        self._logger.error(
            "IMS call failed with status code {error_code}".format(error_code=response.status_code))
        content = json.loads(response.content)
        # When error is returned with no description
        if not content.get("error_description", None) or content["error_description"].isspace():
            content["error_description"] = content.get("error", None)
        # Special handling for invalid token and certificate expiry cases
        if "invalid_token"==content.get("error", None):
            if "Could not match JWT signature to any of the bindings"==content.get("error_description",None):
                content["error_description"] = custom_error_messages["imsCertificateExpiredErrorMessage"]
            else:
                content["error_description"] = custom_error_messages["imsInvalidTokenGenericErrorMessage"]
        raise OperationException(message="Error response received for IMS request",
                                 status_code=response.status_code,
                                 error_code=content.get("error", None),
                                 error_message=content.get("error_description", None),
                                 request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, True))

    def _prepare_jwt(self):
        audience = "{base_uri}/{audience_suffix}{client_id}".format(
            base_uri=self.service_account_configuration.ims_base_uri,
            audience_suffix=ServiceConstants.JWT_AUDIENCE_SUFFIX,
            client_id=self.service_account_configuration.client_id
        )
        payload = {
            'sub': self.service_account_configuration.account_id,
            'iss': self.service_account_configuration.organization_id,
            'aud': audience,
            'exp': int((datetime.now() + timedelta(days=1)).timestamp() * 1000),
            self.service_account_configuration.claim: True
        }

        try:
            return jwt.encode(
                payload=payload,
                key=self.service_account_configuration.private_key,
                algorithm="RS256",
            )
        except:
            self._logger.exception("Exception encountered while signing JWT")
            raise SdkException("Exception in signing jwt token", sys.exc_info())
