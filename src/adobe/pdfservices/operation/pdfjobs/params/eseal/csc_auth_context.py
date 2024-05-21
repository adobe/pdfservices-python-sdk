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


class CSCAuthContext:
    """
    Parameters for representing CSC authorization context.
    """

    @enforce_types
    def __init__(self, access_token: str, token_type: str = 'Bearer'):
        """
        Constructs a new instance of :samp:`CSCAuthContext`

        :param access_token: The service access token used to authorize access to the CSC provider hosted APIs.
            Cannot be None.
        :type access_token: str
        :param token_type: The type of service access token used to authorize access to the CSC provider hosted APIs.
            Default value is "Bearer".
        :type token_type: str
        """
        self._access_token = access_token
        self._token_type = token_type

    def get_access_token(self):
        """
        :return: The service access token.
        :rtype: str
        """
        return self._access_token

    def get_token_type(self):
        """
        :return: The type of service access token used.
        :rtype: str
        """
        return self._token_type

    def to_dict(self):
        return {
            'accessToken': self._access_token,
            'tokenType': self._token_type,
        }
