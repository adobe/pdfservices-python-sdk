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
import os
from abc import ABC

from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.util import path_util, file_utils
from .credentials import Credentials
from ..internal.util.validation_util import is_empty


def _is_valid(value, name):
    if is_empty(value):
        raise ValueError(name + " must not be blank")
    return value


class ServiceAccountCredentials(Credentials, ABC):
    """
    Service Account credentials allow your application to call PDF Tools Extract API on behalf of the application itself,
    or on behalf of an enterprise organization. For getting the credentials,
    `Click Here <https://www.adobe.com/go/pdfextractapi_requestform>`_.
    """

    # TODO Can this constructor be excluded from documentation
    def __init__(self, client_id, client_secret, private_key, organization_id, account_id,
                 ims_base_uri=ServiceConstants.JWT_BASE_URI, claim=None):

        self._client_id = _is_valid(client_id, "client_id")
        self._client_secret = _is_valid(client_secret, "client_secret")
        self._private_key = _is_valid(private_key, "private_key")
        self._organization_id = _is_valid(organization_id, "organization_id")
        self._account_id = _is_valid(account_id, "account_id")
        self.ims_base_uri = ServiceConstants.JWT_BASE_URI if not ims_base_uri else ims_base_uri
        if not claim:
            format_str = "{base}{claim}" if self.ims_base_uri.endswith("/") else "{base}/{claim}"
            claim = format_str.format(
                base=self.ims_base_uri,
                claim=ServiceConstants.JWT_CLAIM
            )
        self._claim = _is_valid(claim, "claim")

    @property
    def client_id(self):
        """ Client Id (API Key) """
        return self._client_id

    @property
    def client_secret(self):
        """  Client Secret"""
        return self._client_secret

    @property
    def private_key(self):
        """  Content of the Private Key (PEM format) """
        return self._private_key

    @property
    def claim(self):
        """ Identifies the Service for which Authorization(Access) Token will be issued"""
        return self._claim

    @property
    def organization_id(self):
        """Identifies the organization(format: org_ident@AdobeOrg) that has been configured for access to PDF Tools API."""
        return self._organization_id

    @property
    def account_id(self):
        """Account ID(format: id@techacct.adobe.com)"""
        return self._account_id

    class Builder:
        """
        Builds a :class:`ServiceAccountCredentials` instance.
        """
        _CLIENT_CREDENTIALS = "client_credentials"
        _CLIENT_ID = "client_id"
        _CLIENT_SECRET = "client_secret"
        _SERVICE_ACCOUNT_CREDENTIALS = "service_account_credentials"
        _PRIVATE_KEY_FILE = "private_key_file"
        _CLAIM = "claim"
        _ORGANIZATION_ID = "organization_id"
        _TECHNICAL_ACCOUNT_ID = "account_id"
        _IMS_BASE_URI = "ims_base_uri"

        def __init__(self):
            self._client_id = None
            self._client_secret = None
            self._private_key = None
            self._account_id = None
            self._organization_id = None
            self._ims_base_uri = ServiceConstants.JWT_BASE_URI
            self._claim = None
            return

        def with_client_id(self, client_id: str):
            """ Set Client ID (API Key)

            :param client_id: Client Id (API Key)
            :type client_id: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            self._client_id = client_id
            return self

        def with_client_secret(self, client_secret: str):
            """ Set Client Secret

            :param client_secret: Client Secret
            :type client_secret: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            self._client_secret = client_secret
            return self

        def with_private_key(self, private_key: str):
            """ Set private key

            :param private_key: Content of the Private Key (PEM format)
            :type private_key: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            self._private_key = private_key
            return self

        def with_organization_id(self, organization_id: str):
            """ Set Organization Id (format: org_ident@AdobeOrg) that has been configured for access to PDF Tools API

            :param organization_id: Organization ID (format: org_ident@AdobeOrg)
            :type organization_id: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            self._organization_id = organization_id
            return self

        def with_account_id(self, account_id: str):
            """ Set Account Id (format: id@techacct.adobe.com)

            :param account_id: Account ID (format: id@techacct.adobe.com)
            :type account_id: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            self._account_id = account_id
            return self

        def from_file(self, credentials_file_path: str):
            """ Sets Service Account Credentials using the JSON credentials file path. All the keys in the JSON structure are optional.

            JSON structure:

            .. code-block:: JSON

                {
                    "client_credentials": {
                    "client_id": "CLIENT_ID",
                    "client_secret": "CLIENT_SECRET"
                  },
                  "service_account_credentials": {
                    "organization_id": "org_ident@AdobeOrg",
                    "account_id": "id@techacct.adobe.com",
                    "private_key_file": "private.key"
                  }
                }

            private_key_file is the path of private key file. It will be looked up in the classpath and the directory of JSON credentials file.

            :param credentials_file_path: JSON credentials file path
            :type credentials_file_path: str
            :return: This Builder instance to add any additional parameters.
            :rtype: ServiceAccountCredentials.Builder
            """
            config_json_str = file_utils.read_conf_file_content(credentials_file_path)
            config_dict = json.loads(config_json_str)
            client_credentials = config_dict.get(self._CLIENT_CREDENTIALS, {})
            self._client_id = client_credentials.get(self._CLIENT_ID, self._client_id)
            self._client_secret = client_credentials.get(self._CLIENT_SECRET, self._client_secret)
            service_account_credentials = config_dict.get(self._SERVICE_ACCOUNT_CREDENTIALS, {})
            self._claim = service_account_credentials.get(self._CLAIM, self._claim)
            self._organization_id = service_account_credentials.get(self._ORGANIZATION_ID, self._organization_id)
            self._ims_base_uri = service_account_credentials.get(self._IMS_BASE_URI, self._ims_base_uri)
            self._account_id = service_account_credentials.get(self._TECHNICAL_ACCOUNT_ID, self._account_id)
            private_key_file_path = service_account_credentials.get(self._PRIVATE_KEY_FILE, None)
            if private_key_file_path:
                # if its not relative to current working directory,
                # create file path with credentials file directory as working directory
                if not os.path.exists(path_util.get_file_path(private_key_file_path)):
                    credentials_file_directory = os.path.dirname(path_util.conf_file_abs_path(credentials_file_path))
                    private_key_file_path = os.path.join(credentials_file_directory, private_key_file_path)
                self._private_key = file_utils.read_conf_file_content(private_key_file_path)
            return self

        def build(self):
            """ Returns a new :class:`ServiceAccountCredentials` instance built from the current state of this builder.

            :return: A ServiceAccountCredentials instance.
            :rtype: ServiceAccountCredentials
            """
            return ServiceAccountCredentials(self._client_id, self._client_secret, self._private_key, self._organization_id,
                                             self._account_id, self._ims_base_uri, self._claim)
