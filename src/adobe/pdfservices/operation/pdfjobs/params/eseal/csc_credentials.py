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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.eseal.csc_auth_context import CSCAuthContext


class CSCCredentials:
    """
    Parameters for representing the CSC Provider based credentials as a subtype
    """

    @enforce_types
    def __init__(self, provider_name: str, credential_id: str, pin: str, csc_auth_context: CSCAuthContext):
        """
        Creates an instance of :samp:`CSCCredentials`.

        :param provider_name: The name of the Trust Service Provider to be used for applying electronic seal.
            Can not be None.
        :type provider_name: str
        :param credential_id: The digital ID stored with the TSP provider to be used for applying electronic seal.
            Can not be None.
        :type credential_id: str
        :param pin: The pin associated with the credential ID. Can not be None.
        :type pin: str
        :param csc_auth_context: The service authorization data required to communicate with the TSP. Can not be None.
        :type csc_auth_context: CSCAuthContext
        """
        self._provider_name = provider_name
        self._credential_id = credential_id
        self._pin = pin
        self._csc_auth_context = csc_auth_context

    def get_csc_auth_context(self):
        """
        :return: The service authorization data.
        :rtype: CSCAuthContext
        """
        return self._csc_auth_context

    def get_credential_id(self):
        """
        :return: The digital ID stored with the TSP provider.
        :rtype: str
        """
        return self._credential_id

    def get_provider_name(self):
        """
        :return: The name of the Trust Service Provider.
        :rtype: str
        """
        return self._provider_name

    def get_pin(self):
        """
        :return: The pin associated with the credential ID.
        :rtype: str
        """
        return self._pin

    def to_dict(self):
        return {
            'credentialId': self._credential_id,
            'providerName': self._provider_name,
            'authorizationContext': {
                'accessToken': self._csc_auth_context.get_access_token(),
                'tokenType': self._csc_auth_context.get_token_type()
            },
            'credentialAuthParameters': {
                'pin': self._pin
            }
        }
