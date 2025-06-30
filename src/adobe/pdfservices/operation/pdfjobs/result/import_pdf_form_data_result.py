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

from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.pdfjobs.result.pdf_services_job_result import PDFServicesJobResult


class ImportPDFFormDataResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`ImportPDFFormDataJob<adobe.pdfservices.operation.pdfjobs.jobs.import_pdf_form_data_job.ImportPDFFormDataJob>`
    """

    def __init__(self, asset: Asset):
        """
        Constructs a new :samp:`ImportPDFFormDataResult` instance.

        :param asset: result asset containing the PDF with imported form data
        :type asset: Asset
        """
        self._asset = asset

    def get_asset(self):
        """
        :return: the result Asset containing the PDF with imported form data
        :rtype: Asset
        """
        return self._asset 