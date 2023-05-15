# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
import json

from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.util import file_utils
from adobe.pdfservices.operation.region import Region


class ClientConfig(object):
    """
    Encapsulates the API request configurations
    """
    _CONNECT_TIMEOUT_KEY = "connectTimeout"
    _READ_TIMEOUT_KEY = "readTimeout"
    _PDF_SERVICES = "pdf_services"
    _PDF_SERVICES_URI = "pdf_services_uri"
    _REGION = "region"

    @staticmethod
    def builder():
        """Creates a new :class:`ClientConfig` builder.

        :return: A ClientConfig.Builder instance.
        :rtype: ClientConfig.Builder
        """
        return ClientConfig.Builder()

    def __init__(self):
        return

    class Builder:
        """
        Builds a :class:`ClientConfig` instance.
        """
        def __init__(self):
            self._connect_timeout = ServiceConstants.HTTP_CONNECT_TIMEOUT
            self._read_timeout = ServiceConstants.HTTP_READ_TIMEOUT
            self._pdf_services_uri = ServiceConstants.PDF_SERVICES_URI

        def with_pdf_services_uri(self, pdf_services_uri: str):
            """Sets the pdf service uri.

            :param pdf_services_uri: PDF service URI.
            :type pdf_services_uri: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ClientConfig.Builder
            """
            self._pdf_services_uri = pdf_services_uri
            return self

        def with_region(self, region: Region):
            """Updates the relevant value for the region.

            :param region: Service region(US or EU). Default value is US.
            :type region: Region
            :return: This Builder instance to add any additional parameters.
            :rtype: ClientConfig.Builder
            """
            self._set_pdf_services_uri_for_region(region)
            return self

        def _set_pdf_services_uri_for_region(self, region: Region):
            """Sets the pdf service uri based on the region.

            :param region: Service region(US or EU).Default value is US.
            :type region: Region
            :return: Region specific pdf_services_uri
            :rtype: str
            """
            if region == 'us':
                self._pdf_services_uri = ServiceConstants.PDF_SERVICES_URI_US
            elif region == 'eu':
                self._pdf_services_uri = ServiceConstants.PDF_SERVICES_URI_EU

        # the time it allows for the client to establish a connection to the server
        def with_connect_timeout(self, connect_timeout: int):
            """Sets the connect timeout. It should be greater than zero.

            :param connect_timeout: determines the timeout in milliseconds until a connection is established in the \
                API calls. Default value is 4000 milliseconds
            :type connect_timeout: int
            :return: This Builder instance to add any additional parameters.
            :rtype: ClientConfig.Builder
            """
            self._connect_timeout = connect_timeout
            return self

        # the time it will wait on a response once connection is estalished
        def with_read_timeout(self, read_timeout: int):
            """Sets the read timeout. It should be greater than zero.

            :param read_timeout: Defines the read timeout in milliseconds, The number of milliseconds the client will \
                wait for the server to send a response after the connection is established.\
                Default value is 10000 milliseconds
            :type read_timeout: int
            :return: This Builder instance to add any additional parameters.
            :rtype: ClientConfig.Builder
            """
            self._read_timeout = read_timeout
            return self

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
                    "region": "eu"
                }
            """
            config_json_str = file_utils.read_conf_file_content(client_config_file_path)
            config_dict = json.loads(config_json_str)
            self._connect_timeout = int(config_dict.get(ClientConfig._CONNECT_TIMEOUT_KEY, self._connect_timeout))
            self._read_timeout = int(config_dict.get(ClientConfig._READ_TIMEOUT_KEY, self._read_timeout))
            region_node = config_dict.get(ClientConfig._REGION)
            self.with_region(region_node)
            pdf_services_config = config_dict.get(ClientConfig._PDF_SERVICES)
            if pdf_services_config:
                pdf_services_uri_node = pdf_services_config.get(ClientConfig._PDF_SERVICES_URI)
                if pdf_services_uri_node:
                    self._pdf_services_uri = pdf_services_uri_node
            return self

        def build(self):
            """
            Returns a new :class:`ClientConfig` instance built from the current state of this builder.

            :return: A ClientConfig instance.
            :rtype: ClientConfig
            """
            from adobe.pdfservices.operation.internal.internal_client_config import InternalClientConfig
            return InternalClientConfig(self._connect_timeout, self._read_timeout, self._pdf_services_uri)