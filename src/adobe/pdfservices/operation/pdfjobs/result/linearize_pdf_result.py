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


class LinearizePDFResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`LinearizePDFJob<adobe.pdfservices.operation.pdfjobs.jobs.linearize_pdf_job.LinearizePDFJob>`
    """

    def __init__(self, asset: Asset):
        """
        Constructs a new :samp:`LinearizePDFResult` instance.

        :param asset: result asset
        :type asset: Asset
        """
        self._asset = asset

    def get_asset(self):
        """
        :return: the result Asset
        :rtype: Asset
        """
        return self._asset
