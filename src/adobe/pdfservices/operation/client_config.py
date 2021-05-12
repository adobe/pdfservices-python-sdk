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

from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.util import file_utils


class ClientConfig(object):
    """
    Encapsulates the API request configurations
    """
    _CONNECT_TIMEOUT_KEY = "connectTimeout"
    _READ_TIMEOUT_KEY = "readTimeout"
    _CPF_SERVICES_KEY = "cpfServices"
    _CPF_SERVICES_OPS_CREATE_KEY = "cpfOpsCreateUri"
    _CPF_EXTRACT_ANALYZER_ID = "cpfExtractAnalyzerId"

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
            self._cpf_ops_create_uri = ServiceConstants.CPF_OPS_CREATE_URI
            self._cpf_extract_analyzer_id = ServiceConstants.CPF_OPS_EXTRACT_ANALYZER_ID

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
                    "readTimeout": "20000"
                }
            """
            config_json_str = file_utils.read_conf_file_content(client_config_file_path)
            config_dict = json.loads(config_json_str)
            self._connect_timeout = int(config_dict.get(ClientConfig._CONNECT_TIMEOUT_KEY, self._connect_timeout))
            self._read_timeout = int(config_dict.get(ClientConfig._READ_TIMEOUT_KEY, self._read_timeout))
            cpf_services_config = config_dict.get(ClientConfig._CPF_SERVICES_KEY, {})
            self._cpf_ops_create_uri = cpf_services_config.get(ClientConfig._CPF_SERVICES_OPS_CREATE_KEY,
                                                               self._cpf_ops_create_uri)
            self._cpf_extract_analyzer_id = cpf_services_config.get(ClientConfig._CPF_EXTRACT_ANALYZER_ID,
                                                                    self._cpf_extract_analyzer_id)
            return self

        def build(self):
            """
            Returns a new :class:`ClientConfig` instance built from the current state of this builder.

            :return: A ClientConfig instance.
            :rtype: ClientConfig
            """
            from adobe.pdfservices.operation.internal.internal_client_config import InternalClientConfig
            return InternalClientConfig(self._connect_timeout, self._read_timeout, self._cpf_ops_create_uri,
                                        self._cpf_extract_analyzer_id)
