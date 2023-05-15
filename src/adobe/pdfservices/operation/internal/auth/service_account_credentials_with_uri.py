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
from adobe.pdfservices.operation.auth.service_account_credentials import ServiceAccountCredentials
from adobe.pdfservices.operation.auth.service_account_credentials import _is_valid


class ServiceAccountCredentialsWithUri(ServiceAccountCredentials):
    """
    Service Account credentials allow your application to call PDF Tools Extract API on behalf of the application itself,
    or on behalf of an enterprise organization. For getting the credentials,
    `Click Here <https://www.adobe.com/go/pdfextractapi_requestform>`_.
    """

    def __init__(self, client_id, client_secret, private_key, organization_id, account_id,
                 pdf_services_uri=ServiceConstants.PDF_SERVICES_URI, ims_base_uri=ServiceConstants.JWT_BASE_URI, claim=None):
        super().__init__(client_id, client_secret, private_key, organization_id, account_id)
        self.ims_base_uri = ServiceConstants.JWT_BASE_URI if not ims_base_uri else ims_base_uri
        if not claim:
            format_str = "{base}{claim}" if self.ims_base_uri.endswith("/") else "{base}/{claim}"
            claim = format_str.format(
                base=self.ims_base_uri,
                claim=ServiceConstants.JWT_CLAIM
            )
        self._claim = _is_valid(claim, "claim")
        self._pdf_services_uri = ServiceConstants.PDF_SERVICES_URI if not pdf_services_uri else pdf_services_uri

    @property
    def pdf_services_uri(self):
        """ PDF Services URI """
        return self._pdf_services_uri

    @property
    def claim(self):
        """ Identifies the Service for which Authorization(Access) Token will be issued"""
        return self._claim

    def get_claim(self):
        return self._claim

    def get_ims_base_uri(self):
        return self.ims_base_uri

    def get_pdf_services_uri(self):
        return self._pdf_services_uri
