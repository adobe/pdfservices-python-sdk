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

from adobe.pdfservices.operation.config.proxy.proxy_authentication_credentials import ProxyAuthenticationCredentials
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.string_util import StringUtil


class UsernamePasswordCredentials(ProxyAuthenticationCredentials):
    """
    Simple
    :class:`ProxyAuthenticationCredentials<adobe.pdfservices.operation.config.proxy.proxy_authentication_credentials.ProxyAuthenticationCredentials>`
    implementation based on a username and password.
    """

    @enforce_types
    def __init__(self, username: str, password: str):
        """
        Constructs an instance of :samp:`UsernamePasswordCredentials`.

        :param username: Username. Cannot be none or empty.
        :type username: str
        :param password: Password. Cannot be none or empty.
        :type password: str
        """
        if StringUtil.is_blank(username):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Username"))
        if StringUtil.is_blank(password):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Password"))

        self._username = username
        self._password = password

    def get_username(self) -> str:
        """
        :return: the username.
        :rtype: str
        """
        return self._username

    def get_password(self) -> str:
        """
        :return: the password.
        :rtype: str
        """
        return self._password

    def from_json(self, json_data: dict):
        """
        Constructs a :samp:`UsernamePasswordCredentials` instance from a dictionary in the specified format.

        .. code-block:: JSON
            {
                "usernamePasswordCredentials": {
                    "username": "username",
                    "password": "password"
                }
            }

        :param json_data: JSON data in the form of a dictionary.
        :type json_data: dict
        """
        self._username = json_data.get("username")
        self._password = json_data.get("password")
        return self
