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

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.config.client_config import ClientConfig
from adobe.pdfservices.operation.internal.auth.auth_factory import AuthenticatorFactory
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator


class ExecutionContext:
    _credentials = None
    _authenticator = None
    _client_config: ClientConfig = None

    def __init__(self, credentials: Credentials, client_config: ClientConfig = None):
        self._credentials = credentials
        if client_config is not None:
            self._client_config: ClientConfig = client_config
        else:
            self._client_config: ClientConfig = ClientConfig()

        self._client_config.validate()
        self._authenticator: Authenticator = AuthenticatorFactory.get_authenticator(credentials,
                                                                                    self._client_config)

    @property
    def client_config(self):
        return self._client_config

    @property
    def authenticator(self):
        return self._authenticator

    @property
    def credentials(self):
        return self._credentials

    def validate(self):
        if not self._client_config:
            raise ValueError("Client Context not initialized before invoking the operation")
        self._client_config.validate()
        if not self._authenticator:
            raise ValueError("Authentication not initialized in the provided context")
