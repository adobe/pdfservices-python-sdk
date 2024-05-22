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


class Permission(Enum):
    """
    Document Permissions for
    :class:`ProtectPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job.ProtectPDFJob>`
    """

    PRINT_LOW_QUALITY = "PRINT_LOW_QUALITY"
    """
    Enables low quality printing of the PDF document
    """

    PRINT_HIGH_QUALITY = "PRINT_HIGH_QUALITY"
    """
    Enables high quality printing of the PDF document
    """

    EDIT_CONTENT = "EDIT_CONTENT"
    """
    Enables all the editing permissions in the PDF document except commenting and page extraction
    """

    EDIT_DOCUMENT_ASSEMBLY = "EDIT_DOCUMENT_ASSEMBLY"
    """
    Enables insertion, deletion and rotation of pages in a PDF document
    """

    EDIT_ANNOTATIONS = "EDIT_ANNOTATIONS"
    """
    Enables additions of comments, digital signatures and filling in of forms in a PDF document
    """

    EDIT_FILL_AND_SIGN_FORM_FIELDS = "EDIT_FILL_AND_SIGN_FORM_FIELDS"
    """
    Enables filling in of forms, digital signature and creation of template pages in a PDF document
    """

    COPY_CONTENT = "COPY_CONTENT"
    """
    Enables copying of content from the PDF document
    """

    def __str__(self):
        return self.value
