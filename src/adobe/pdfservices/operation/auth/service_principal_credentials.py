# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import json
import os
from abc import ABC

from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.util import path_util, file_utils
from .credentials import Credentials, _is_valid


class ServicePrincipalCredentials(Credentials, ABC):
    """
         OAuth Server-to-Server based Service Principal credentials allow your application to call PDF Services API on behalf of the application itself,
         or on behalf of an enterprise organization. For getting the credentials,
         `Click Here <https://www.adobe.com/go/dcsdks_credentials?ref=getStartedWithServicesSdk>`_.
     """

    def __init__(self, client_id, client_secret):
        self._client_id = _is_valid(client_id, 'client_id')
        self._client_secret = _is_valid(client_secret, 'client_secret')

    @property
    def client_id(self):
        """ Client Id (API Key) """
        return self._client_id

    @property
    def client_secret(self):
        """  Client Secret"""
        return self._client_secret

    class Builder:
        """
        Builds a :class:`ServicePrincipalCredentials` instance.
        """
        _CLIENT_ID = "client_id"
        _CLIENT_SECRET = "client_secret"

        def __init__(self):
            self._client_id = None
            self._client_secret = None
            return

        def with_client_id(self, client_id: str):
            """ Set Client ID (API Key)

            :param client_id: Client Id (API Key)
            :type client_id: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServicePrincipalCredentials.Builder
            """
            self._client_id = client_id
            return self

        def with_client_secret(self, client_secret: str):
            """ Set Client Secret

            :param client_secret: Client Secret
            :type client_secret: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServicePrincipalCredentials.Builder
            """
            self._client_secret = client_secret
            return self

        def build(self):
            """ Returns a new :class:`ServicePrincipalCredentials` instance built from the current state of this builder.

            :return: A ServicePrincipalCredentials instance.
            :rtype: ServicePrincipalCredentials
            """

            return ServicePrincipalCredentials(self._client_id, self._client_secret)
