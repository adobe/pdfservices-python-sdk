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


class Credentials(ABC):
    """
    Marker base class for different types of credentials. Currently it supports only :class:`.ServiceAccountCredentials`.
    The factory methods within this class can be used to create instances of credentials classes.
    """

    @staticmethod
    def service_account_credentials_builder():
        """ Creates a new :class:`.ServiceAccountCredentials` builder.

        :return: An instance of ServiceAccountCredentials Builder.
        :rtype: ServiceAccountCredentials.Builder
        """
        from adobe.pdfservices.operation.auth.service_account_credentials import ServiceAccountCredentials
        return ServiceAccountCredentials.Builder()
