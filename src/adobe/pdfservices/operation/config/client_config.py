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

from adobe.pdfservices.operation.config.proxy.proxy_server_config import ProxyServerConfig
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.constants.pdf_services_uri import PDFServicesURI
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.util import file_utils
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.string_util import StringUtil
from adobe.pdfservices.operation.region import Region


class ClientConfig:
    """
    Encapsulates the API request configurations.
    """
    _PDF_SERVICES = "pdfServices"
    _PDF_SERVICES_URI = "pdfServicesUri"
    _CONNECT_TIMEOUT_KEY = "connectTimeout"
    _READ_TIMEOUT_KEY = "readTimeout"
    _PROXY_HOST = "host"
    _PROXY_SERVER_CONFIG = "proxyServerConfig"
    _PROXY_PORT = "port"
    _PROXY_SCHEME = "proxyScheme"
    _REGION = "region"
    _PROXY_CREDENTIALS = "usernamePasswordCredentials"
    _PROXY_USERNAME = "username"
    _PROXY_PASSWORD = "password"

    @enforce_types
    def __init__(self, *,
                 connect_timeout: int = ServiceConstants.HTTP_CONNECT_TIMEOUT,
                 read_timeout: int = ServiceConstants.HTTP_READ_TIMEOUT,
                 region: Region = Region.US,
                 proxy_server_config: ProxyServerConfig = None):
        """
        Constructs an instance of :samp:`ClientConfig`.

        :param connect_timeout: determines the timeout in milliseconds until a connection is established in the API
            calls. Default value is 4000 milliseconds.
        :type connect_timeout: int
        :param read_timeout: Defines the read timeout in milliseconds, The number of milliseconds the client will \
                wait for the server to send a response after the connection is established.\
                Default value is 10000 milliseconds
        :type read_timeout: int
        :param region: Default value is US.
        :type region: Region
        :param proxy_server_config: Sets the configuration for proxy server.
        :type proxy_server_config: ProxyServerConfig
        """
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._pdf_services_uri = PDFServicesURI.get_uri_for_region(region)
        self._proxy_server_config = proxy_server_config

    def get_pdf_services_uri(self):
        """
        :return: The PDF Service URI used.
        :rtype: str
        """
        return self._pdf_services_uri

    def get_connect_timeout(self):
        """
        :return: Connect timeout.
        :rtype: int
        """
        return self._connect_timeout / 1000 if self._connect_timeout else None

    def get_read_timeout(self):
        """
        :return: Read timeout.
        :rtype: int
        """
        return self._read_timeout / 1000 if self._read_timeout else None

    def get_proxy_server_config(self):
        """
        :return: Proxy server config used.
        :rtype: ProxyServerConfig
        """
        return self._proxy_server_config

    def validate(self):
        """
        Validator for the created client config.
        """
        if self._read_timeout <= 0:
            raise ValueError(
                "Invalid value for read timeout {timeout}. Must be valid integer greater than 0".format(
                    timeout=self._read_timeout))

        if self._connect_timeout <= 0:
            raise ValueError(
                "Invalid value for connect timeout {timeout}. Must be valid integer greater than 0".format(
                    timeout=self._connect_timeout))

        if self._proxy_server_config is not None:
            if int(self._proxy_server_config.get_port()) <= 0:
                raise ValueError("Invalid value for proxy port. Must be valid integer greater than 0")

            if StringUtil.is_blank(self._proxy_server_config.get_host()):
                raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Host"))

    def from_file(self, client_config_file_path: str):
        """
        Sets the connect timeout and read timeout using the JSON client config file path. \
        All the keys in the JSON structure are optional.

        :param client_config_file_path: JSON client config file path
        :type client_config_file_path: str
        :return: This Builder instance to add any additional parameters.
        :rtype: ClientConfig.Builder

        JSON structure:

        .. code-block:: JSON

            {
                "connectTimeout": "4000",
                "readTimeout": "20000",
                "proxyServerConfig": {
                    "host": "127.0.0.1",
                    "port": "8080",
                    "scheme": "https",
                    "usernamePasswordCredentials": {
                        "username": "username",
                        "password": "password"
                        }
                },
                "region": "EU"
            }
        """
        try:
            config_json_str = file_utils.read_conf_file_content(client_config_file_path)
            config_dict = json.loads(config_json_str)

            self._connect_timeout = int(config_dict.get(ClientConfig._CONNECT_TIMEOUT_KEY, self._connect_timeout))

            self._read_timeout = int(config_dict.get(ClientConfig._READ_TIMEOUT_KEY, self._read_timeout))

            region_node = config_dict.get(ClientConfig._REGION)
            if region_node:
                self._pdf_services_uri = PDFServicesURI.get_uri_for_region(region_node)

            pdf_services_config = config_dict.get(ClientConfig._PDF_SERVICES)
            if pdf_services_config:
                pdf_services_uri_node = pdf_services_config.get(ClientConfig._PDF_SERVICES_URI)
                if pdf_services_uri_node:
                    self._pdf_services_uri = pdf_services_uri_node

            proxy_server_config = config_dict.get(ClientConfig._PROXY_SERVER_CONFIG)
            if proxy_server_config:
                self._proxy_server_config = ProxyServerConfig("host").from_json(proxy_server_config)

            return self
        except Exception as e:
            raise ValueError("Error while reading client config file: " + str(e))
