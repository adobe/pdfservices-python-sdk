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
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_locale import OCRSupportedLocale
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_supported_type import OCRSupportedType
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class OCRParams(PDFServicesJobParams):
    """
    Parameters for converting PDF to a searchable PDF using
    :class:`OCRPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.ocr_pdf_job.OCRPDFJob`
    """

    @enforce_types
    def __init__(self, *, ocr_locale: OCRSupportedLocale = OCRSupportedLocale.EN_US,
                 ocr_type: OCRSupportedType = OCRSupportedType.SEARCHABLE_IMAGE):
        """
        Constructs a new :samp:`OCRParams` instance.

        :param ocr_locale: Input language to be used for OCR. (Optional, use key-value)
        :type ocr_locale: OCRSupportedLocale
        :param ocr_type: OCR type. (Optional, use key-value)
        :type ocr_type: OCRSupportedType
        """
        self.__ocr_locale = ocr_locale
        self.__ocr_type = ocr_type

    def get_ocr_locale(self):
        """
        :return: OCRSupportedLocale to be used for OCR.
        :rtype: OCRSupportedLocale
        """
        return self.__ocr_locale

    def get_ocr_type(self):
        """
        :return: OCRSupportedType to be used for OCR.
        :rtype: OCRSupportedType
        """
        return self.__ocr_type
