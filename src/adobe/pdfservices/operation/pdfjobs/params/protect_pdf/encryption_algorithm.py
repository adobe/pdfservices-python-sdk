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


class EncryptionAlgorithm(Enum):
    """
    Supported encryption algorithms for
    :class:`ProtectPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job.ProtectPDFJob>`
    """

    AES_128 = "AES_128"
    """
    Represents AES-128 encryption algorithm
    """

    AES_256 = "AES_256"
    """
    Represents AES-256 encryption algorithm
    """

    def __str__(self):
        return self.value
