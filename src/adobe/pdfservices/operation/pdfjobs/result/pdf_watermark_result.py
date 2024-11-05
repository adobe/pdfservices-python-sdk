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


class PDFWatermarkResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`PDFWatermarkJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_watermark_job.PDFWatermarkJob>`.
    """

    def __init__(self, pdf_watermark: Asset):
        """
        Constructs a new :samp:`PDFWatermarkResult` instance.

        :param asset: Result asset
        :type asset: Asset
        """
        self._pdf_watermark = pdf_watermark

    def get_asset(self):
        """
        :return: Returns watermark PDF asset, if an internal asset was used as input PDF.
        :rtype: Asset
        """
        return self._pdf_watermark
