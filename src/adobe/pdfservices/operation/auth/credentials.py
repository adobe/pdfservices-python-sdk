# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from abc import ABC
from adobe.pdfservices.operation.internal.util.validation_util import is_empty


def _is_valid(value, name):
    if is_empty(value):
        raise ValueError(f'{name} must not be blank')
    return value


class Credentials(ABC):
    """
    Marker base class for different types of credentials. Currently it supports :class:`.ServiceAccountCredentials` and :class:`.ServicePrincipalCredentials`.
    The factory methods within this class can be used to create instances of credentials classes.
    """

    @staticmethod
    def service_account_credentials_builder():
        """ Creates a new :class:`.ServiceAccountCredentials` builder.

        :return: An instance of ServiceAccountCredentials Builder.
        :rtype: ServiceAccountCredentials.Builder

        .. deprecated:: 2.3.0
            Notice: JWT based service account credentials has been deprecated. Please use OAuth Server-to-Server based :class:`.ServicePrincipalCredentials`.
        """
        from adobe.pdfservices.operation.auth.service_account_credentials import ServiceAccountCredentials
        return ServiceAccountCredentials.Builder()

    @staticmethod
    def service_principal_credentials_builder():
        """ Creates a new :class:`.ServicePrincipalCredentials` builder.

        :return: An instance of ServicePrincipalCredentials Builder.
        :rtype: ServicePrincipalCredentials.Builder
        """
        from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
        return ServicePrincipalCredentials.Builder()
