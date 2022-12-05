# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from adobe.pdfservices.operation.client_config import ClientConfig
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants


class InternalClientConfig(ClientConfig):

    #TODO Clientconfig builder also sets the default values. Figure out if it can be done only at one place
    # Setting default values is required for when client config is not provided explicitly.
    def __init__(self, connect_timeout: int = ServiceConstants.HTTP_CONNECT_TIMEOUT,
                 read_timeout: int = ServiceConstants.HTTP_READ_TIMEOUT,
                 pdf_services_uri: str = ServiceConstants.PDF_SERVICES_URI):

        super().__init__()
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._pdf_services_uri = pdf_services_uri

    def get_pdf_services_uri(self):
        return self._pdf_services_uri

    def get_connect_timeout(self):
        return self._connect_timeout/1000 if self._connect_timeout else None

    def get_read_timeout(self):
        return self._read_timeout/1000 if self._read_timeout else None

    def validate(self):
        if self._read_timeout <= 0:
            raise ValueError("Invalid value for read timeout {timeout}. Must be valid integer greater than 0".format(timeout=self._read_timeout))

        if self._connect_timeout <= 0:
            raise ValueError("Invalid value for connect timeout {timeout}. Must be valid integer greater than 0".format(
                timeout=self._connect_timeout))
