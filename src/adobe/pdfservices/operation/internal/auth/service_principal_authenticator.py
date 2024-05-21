# Copyright 2024 Adobe
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.

import json
import logging
import sys
import threading
from datetime import datetime
from http import HTTPStatus

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import SdkException, ServiceApiException
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.auth.session_token import SessionToken
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.constants.service_constants import custom_error_messages
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil


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
        self.proxy_server_config = client_config.get_proxy_server_config()

        # thread locking to avoid refreshing token multiple times in multi threaded cases
        self.lock = threading.Lock()

    def session_token(self):
        """ Access token for the PDF Services API """
        with self.lock:
            if self.token:
                if self.time_to_expire() > 2:
                    return self.token
            self._logger.debug(
                "Refreshing access token with creation time: {creation_time} minutes".format(
                    creation_time=datetime.now()))
            return self.refresh_token()

    def time_to_expire(self):
        """ Time remaining in minutes till token expiry """
        return int((self.token.expired_at.timestamp() - datetime.now().timestamp()) / 60)

    def refresh_token(self):
        """ Refreshes the access token sent to PDF Services API """
        url = "{token_endpoint}/{ims_proxy_token_endpoint}".format(
            token_endpoint=self.token_endpoint,
            ims_proxy_token_endpoint='token'
        )
        access_token_request_payload = {"client_id": self.service_principal_configuration.get_client_id(),
                                        "client_secret": self.service_principal_configuration.get_client_secret()}

        try:
            http_request = HttpRequest(http_method=HttpMethod.POST, request_key=RequestKey.AUTHN, url=url,
                                       data=access_token_request_payload, headers={},
                                       proxies=self.proxy_server_config)
            response = http_client.process_request(http_request=http_request, success_status_codes=[HTTPStatus.OK],
                                                   error_response_handler=self.handle_ims_failure)

            content = json.loads(response.content)
            self.token = SessionToken(content['access_token'], content['expires_in'] * 1000)
        except ServiceApiException as ex:
            raise ex
        except Exception:
            raise SdkException("Exception in fetching access token", sys.exc_info())
        return self.token

    def get_api_key(self):
        """ API key for Service Principle credentials """
        return self.service_principal_configuration.get_client_id()

    def handle_ims_failure(self, response):
        """ Handling of IMS failure during call to PDF Services API """

        self._logger.error(
            "IMS call failed with status code {error_code}".format(error_code=response.status_code))
        content = json.loads(response.content)
        # When error is returned with no description
        if not content.get("error_description", None) or content["error_description"].isspace():
            content["error_description"] = content.get("error", None)
        # Special handling for invalid token and certificate expiry cases
        if "invalid_token" == content.get("error", None):
            if "Could not match signature to any of the bindings" == content.get("error_description", None):
                content["error_description"] = custom_error_messages["imsCertificateExpiredErrorMessage"]
            else:
                content["error_description"] = custom_error_messages["imsInvalidTokenGenericErrorMessage"]
        raise OperationException(message="Error response received for IMS request",
                                 status_code=response.status_code,
                                 error_code=content.get("error", None),
                                 error_message=content.get("error_description", None),
                                 request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, True))
