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

from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.auth.service_token_credentials import ServiceTokenCredentials
from adobe.pdfservices.operation.internal.auth.session_token import SessionToken


class ServiceTokenAuthenticator(Authenticator):

    def __init__(self, service_token_credentials: ServiceTokenCredentials):
        self._service_token_credentials = service_token_credentials
        self._session_token = SessionToken(service_token_credentials.get_token(), None)

    def session_token(self) -> SessionToken:
        return self._session_token

    def refresh_token(self) -> SessionToken:
        return self._session_token

    def get_api_key(self) -> str:
        return self._service_token_credentials.get_client_id()
