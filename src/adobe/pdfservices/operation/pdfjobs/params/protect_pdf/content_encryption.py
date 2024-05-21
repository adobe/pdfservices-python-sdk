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


class ContentEncryption(Enum):
    """
    Supported types of content to encrypt for
    :class:`ProtectPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job.ProtectPDFJob>`
    """

    ALL_CONTENT = "ALL_CONTENT"
    """
    Encrypts all the content of the PDF file
    """

    ALL_CONTENT_EXCEPT_METADATA = "ALL_CONTENT_EXCEPT_METADATA"
    """
    Encrypts all the content except the metadata of the PDF file
    """

    ONLY_EMBEDDED_FILES = "ONLY_EMBEDDED_FILES"
    """
    Encrypts only embedded files
    """

    def __str__(self):
        return self.value
