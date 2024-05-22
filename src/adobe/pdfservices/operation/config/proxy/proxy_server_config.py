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
from adobe.pdfservices.operation.config.proxy.proxy_scheme import ProxyScheme
from adobe.pdfservices.operation.config.proxy.username_password_credentials import UsernamePasswordCredentials
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types


class ProxyServerConfig:
    """
    Encapsulates the proxy server configurations.
    """

    HTTP_PORT = 80
    """
    Represents default port for HTTP scheme.
    """

    HTTPS_PORT = 443
    """
    Represents default port for HTTPS scheme.
    """

    @enforce_types
    def __init__(self,
                 host: str, *,
                 port: int = None,
                 scheme: ProxyScheme = ProxyScheme.HTTP,
                 credentials: ProxyAuthenticationCredentials = None):
        """
        Creates an instance of :samp:`ProxyServerConfig`.

        :param host: Host name. (Optional, use key-value)
        :type host: str
        :param port: port number of proxy server. It should be greater than 0. Scheme's default port is used if not
            provided. (Optional, use key-value)
        :type port: int
        :param scheme: scheme of proxy server. Possible values are HTTP and HTTPS. Default value is HTTP. (Optional,
            use key-value)
        :type scheme: ProxyScheme
        :param credentials: ProxyAuthenticationCredentials} instance. (Optional, use key-value)
        :type credentials: ProxyAuthenticationCredentials
        """
        self._host = host
        self._scheme = scheme
        self._port = port if port is not None else self.get_port_based_on_scheme(self._scheme)
        self._credentials = credentials

    def get_host(self):
        """
        :return: the host name of proxy server.
        :rtype: str
        """
        return self._host

    def get_port(self):
        """
        :return: the port number of proxy server.
        :rtype: int
        """
        return self._port

    def get_proxy_scheme(self):
        """
        :return: the scheme of proxy server.
        :rtype: ProxyScheme
        """
        return self._scheme

    def get_credentials(self):
        """
        :return: the credentials for authenticating with a proxy server.
        :rtype: ProxyAuthenticationCredentials
        """
        return self._credentials

    @classmethod
    def get_port_based_on_scheme(cls, scheme: ProxyScheme):
        """
        Used internally by the SDK.
        """
        if scheme == ProxyScheme.HTTP:
            return cls.HTTP_PORT
        elif scheme == ProxyScheme.HTTPS:
            return cls.HTTPS_PORT
        else:
            return cls.HTTP_PORT

    def proxy_config_map(self) -> dict[str, str]:
        """
        Used internally by the SDK.
        """
        if self._credentials is not None:
            if isinstance(self._credentials, UsernamePasswordCredentials):
                # Proxy URL
                proxy_url = f'{self._scheme.value}://{self._credentials.get_username()}:{self._credentials.get_password()}@{self._host}:{self._port.__str__()}'
                return {
                    "http": proxy_url,
                    "https": proxy_url
                }
        else:
            proxy_url = f'{self._scheme.value}://{self._host}:{self._port.__str__()}'
            return {
                "http": proxy_url,
                "https": proxy_url
            }

    def from_json(self, json_data: dict):
        """
        Creates a proxy server instance from a json file.

        .. code-block:: JSON

            {
            "proxyServerConfig": {
                    "host": "127.0.0.1",
                    "port": "8080",
                    "scheme": "https",
                    "usernamePasswordCredentials": {
                        "username": "username",
                        "password": "password"
                    }
                },
            }

        :param json_data: A dictionary containing proxy server config in the specified format.
        :type json_data: dict
        """
        self._host = json_data.get("host")
        self._port = json_data.get("port")
        self._scheme = ProxyScheme.get(json_data.get("scheme"))
        credentials = json_data.get("credentials")
        if credentials is not None:
            self._credentials = UsernamePasswordCredentials().from_json(credentials)
        return self
