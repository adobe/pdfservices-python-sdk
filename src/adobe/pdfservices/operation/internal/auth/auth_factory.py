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
from adobe.pdfservices.operation.internal.auth.service_principal_authenticator import ServicePrincipalAuthenticator
from adobe.pdfservices.operation.internal.auth.service_token_authenticator import ServiceTokenAuthenticator
from adobe.pdfservices.operation.internal.auth.service_token_credentials import ServiceTokenCredentials


class AuthenticatorFactory:

    @staticmethod
    def get_authenticator(credential: Credentials, client_config: ClientConfig):
        if isinstance(credential, ServicePrincipalCredentials):
            return ServicePrincipalAuthenticator(credential, client_config)
        if isinstance(credential, ServiceTokenCredentials):
            return ServiceTokenAuthenticator(credential)
        else:
            raise ValueError("Invalid Credentials provided as argument")
