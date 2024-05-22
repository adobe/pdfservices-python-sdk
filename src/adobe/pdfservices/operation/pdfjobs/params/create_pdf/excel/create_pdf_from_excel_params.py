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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.create_pdf.CreatePDFParams import CreatePDFParams
from adobe.pdfservices.operation.pdfjobs.params.create_pdf.excel.document_language import DocumentLanguage


class CreatePDFFromExcelParams(CreatePDFParams):

    @enforce_types
    def __init__(self, *, document_language: DocumentLanguage = DocumentLanguage.EN_US,
                 create_tagged_pdf: bool = False):
        """
        Constructs a new instance of :samp:`CreatePDFFromExcelParams`.

        :param document_language: Sets office preferred editing language to be used for conversion; can not be None.
        :type document_language: DocumentLanguage
        :param create_tagged_pdf: Whether to create a tagged PDF. The default value is false. (Optional, use key-value)
        :type create_tagged_pdf: bool
        """
        super().__init__()
        self.__document_language = document_language
        self.__create_tagged_pdf = create_tagged_pdf

    def get_create_tagged_pdf(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        return self.__create_tagged_pdf

    def get_document_language(self):
        """
        :return: Language of the input document.
        :rtype: DocumentLanguage
        """
        return self.__document_language
