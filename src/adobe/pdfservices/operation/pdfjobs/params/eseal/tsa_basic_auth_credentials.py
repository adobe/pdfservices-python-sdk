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


class TSABasicAuthCredentials:
    """
    Parameters specifying options related to the time stamp authority credentials required for
    :class:`RFC3161TSAOptions<adobe.pdfservices.operation.pdfjobs.params.eseal.RFC3161_tsa_options.RFC3161TSAOptions>`
    """

    @enforce_types
    def __init__(self, username: str, password: str):
        """
        Constructs a :samp:`TSABasicAuthCredentials` instance.

        :param username: username to be used for timestamping
        :type username: str
        :param password: password to be used for timestamping
        :type password: str
        """
        self._username = username
        self._password = password

    def get_username(self):
        """
        Returns the intended username to be used for timestamping.

        :return: The username
        :rtype: str
        """
        return self._username

    def get_password(self):
        """
        Returns the intended password to be used for timestamping.

        :return: The password
        :rtype: str
        """
        return self._password

    def to_dict(self):
        """
        Returns a dictionary representation of the TSABasicAuthCredentials instance.

        :return: A dictionary representing the TSABasicAuthCredentials instance
        """
        return {
            "username": self._username,
            "password": self._password
        }
