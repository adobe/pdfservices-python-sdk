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
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_ocr_locale import ExportOCRLocale
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import ExportPDFTargetFormat
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class ExportPDFParams(PDFServicesJobParams):
    """
    Parameters for exporting a source PDF file to a supported format using
    :class:`ExportPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job.ExportPDFJob>`
    """

    @enforce_types
    def __init__(self, target_format: ExportPDFTargetFormat, *,
                 ocr_lang: ExportOCRLocale = ExportOCRLocale.EN_US):
        """
        Constructs a new :samp:`ExportPDFParams` instance.

        :param target_format: Target format to which the source PDF file will be exported; can not be None
        :type target_format: ExportPDFTargetFormat
        :param ocr_lang: Sets OCR Locale level to be used for Export PDF. (Optional, use key-value)
        :type ocr_lang: ExportOCRLocale
        """
        self.target_format = target_format
        self.ocr_lang = ocr_lang

    def get_target_format(self):
        """
        :return: Returns the target format to which the source PDF file will be exported.
        :rtype: ExportPDFTargetFormat
        """
        return self.target_format

    def get_ocr_lang(self):
        """
        :return: Returns the OCR Locale to be used for Export PDF.
        :rtype: ExportOCRLocale
        """
        return self.ocr_lang
