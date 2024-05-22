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

from enum import Enum


class SignatureFormat(Enum):
    """
    Supported signature formats to create electronic seal required for
    :class:`PDFElectronicSealParams<adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params.PDFElectronicSealParams>`.
    """

    PADES = 'PADES'
    """
    Represents PADES format.
    """

    PKCS7 = 'PKCS7'
    """
    Represents PKCS7 format.
    """

    def __init__(self, signature_format: str):
        self.signature_format = signature_format

    def get_signature_format(self):
        """
        :return: String value of SignatureFormat
        :rtype: str
        """
        return self.signature_format
