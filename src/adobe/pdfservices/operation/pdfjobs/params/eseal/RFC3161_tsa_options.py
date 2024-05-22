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

from typing import Optional

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.eseal.tsa_basic_auth_credentials import TSABasicAuthCredentials
from adobe.pdfservices.operation.pdfjobs.params.eseal.tsa_options import TSAOptions


class RFC3161TSAOptions(TSAOptions):
    """
    Parameters specifying RFC3161 compliant time stamp authority options required for
    :class:`PDFElectronicSealParams<adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params.PDFElectronicSealParams>`.
    """

    @enforce_types
    def __init__(self, url: str, *,
                 tsa_basic_auth_credentials: Optional[TSABasicAuthCredentials] = None):
        """
        Constructs a new :samp:`RFC3161TSAOptions` instance from url.

        :param url: url to be used for timestamping, can not be None.
        :type url: str
        :param tsa_basic_auth_credentials: Credentials to be used for timestamping. (Optional, use key-value)
        :type tsa_basic_auth_credentials: TSABasicAuthCredentials
        """
        self._url = url
        self._tsa_basic_auth_credentials = tsa_basic_auth_credentials

    def get_url(self):
        """
        Returns the timestamp url to be used.

        :return: The timestamp url
        :rtype: str
        """
        return self._url

    def get_tsa_basic_auth_credentials(self):
        """
        Returns the intended TSA authorization credentials to be used.

        :return: A TSABasicAuthCredentials instance
        :rtype: TSABasicAuthCredentials
        """
        return self._tsa_basic_auth_credentials

    def to_dict(self):
        """
        Returns a dictionary representation of the RFC3161TSAOptions instance.

        :return: A dictionary representing the RFC3161TSAOptions instance
        """
        tsa_options = {
            "url": self._url
        }
        if self._tsa_basic_auth_credentials is not None:
            tsa_options["credentialAuthParameters"] = self._tsa_basic_auth_credentials.to_dict()
        return tsa_options
