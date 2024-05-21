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


class DocumentLevelPermission(Enum):
    """
    A mapping of Document Level Permission used in
    :class:`PDFElectronicSealParams<adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params.PDFElectronicSealParams>`.
    """

    NO_CHANGES_ALLOWED = "NO_CHANGES_ALLOWED"
    """
    Represents NO_CHANGES_ALLOWED document level permission.
    No changes to the output document are permitted.
    """

    FORM_FILLING = "FORM_FILLING"
    """
    Represents FORM_FILLING document level permission.
    Allowed changes in output document are filling in forms, instantiating page templates, and performing approval
    signatures.
    """

    FORM_FILLING_AND_ANNOTATIONS = "FORM_FILLING_AND_ANNOTATIONS"
    """
    Represents FORM_FILLING_AND_ANNOTATIONS document level permission.
    In addition to changes allowed in FORM_FILLING, annotation creation, deletion, and modification are also allowed.
    """

    def __str__(self):
        return self.value
