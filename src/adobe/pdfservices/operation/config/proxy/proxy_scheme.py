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

from enum import Enum


class ProxyScheme(Enum):
    """
    Supported scheme types for
    :class:`ProxyServerConfig<adobe.pdfservices.operation.config.proxy.proxy_server_config.ProxyServerConfig>`.
    """

    HTTP = "http"
    """
    Represents HTTP scheme.
    """

    HTTPS = "https"
    """
    Represents HTTPS scheme.
    """

    def __str__(self):
        """
        :return: String representation of proxy scheme.
        :rtype: str
        """
        return self.value

    @classmethod
    def get(cls, proxy_scheme):
        """
        Returns the instance of :samp:`ProxyScheme` for the input string.

        :param proxy_scheme: String value of the scheme.
        :type proxy_scheme: str
        :return: the instance of ProxyScheme for the input string.
        :rtype: ProxyScheme
        """
        for scheme in cls:
            if scheme.value == proxy_scheme.lower():
                return scheme
        raise ValueError(f"Invalid value for proxy scheme {proxy_scheme}")
