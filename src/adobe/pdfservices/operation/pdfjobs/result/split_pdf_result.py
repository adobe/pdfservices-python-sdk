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


class SplitPDFResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`SplitPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.split_pdf_job.SplitPDFJob>`.
    """

    def __init__(self, assets: [], asset: Asset):
        """
        Constructs a new :samp:`SplitPDFResult` instance

        :param assets: List of result assets
        :type assets: list
        :param asset: result asset, enclosing zipped output result
        :type asset: Asset
        """
        self._assets = assets
        self._asset = asset

    def get_assets(self):
        """
        :return: Returns the list of result assets, if an internal asset was used as input PDF.
        :rtype: list
        """
        return self._assets

    def get_asset(self):
        """
        :return: The zipped asset associated with the
            :class:`SplitPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.split_pdf_job.SplitPDFJob>` result, if an
            external asset was used as input PDF.
        :rtype: Asset
        """
        return self._asset
