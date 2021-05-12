# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from adobe.pdfservices.operation.auth.service_account_credentials import ServiceAccountCredentials
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders

from adobe.pdfservices.operation.internal.auth.auth_factory import AuthenticatorFactory
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.internal_client_config import InternalClientConfig


class InternalExecutionContext(ExecutionContext):
    _credentials = None
    authenticator = None
    _client_config: InternalClientConfig = None

    def __init__(self, credentials, client_config):
        if isinstance(credentials, ServiceAccountCredentials):
            self._credentials = credentials
            if isinstance(client_config, InternalClientConfig):
                self._client_config = client_config
            else:
                self._client_config = InternalClientConfig()
            self._client_config.validate()
            self.authenticator = AuthenticatorFactory.get_authenticator(self._credentials)
        else:
            raise ValueError("Invalid Credentials provided as argument")

    @property
    def client_config(self):
        return self._client_config

    def credentials(self):
        return self._credentials

    def validate(self):
        if not self._client_config:
            raise ValueError("Client Context not initialized before invoking the operation")
        self._client_config.validate()
        if not self.authenticator:
            raise ValueError("Authentication not initialized in the provided context")
