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
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class ReorderPagesParams(PDFServicesJobParams):
    """
    Parameters for reordering a pdf using
    :class:`ReorderPagesJob<adobe.pdfservices.operation.pdfjobs.jobs.reorder_pages_job.ReorderPagesJob>`
    """

    @enforce_types
    def __init__(self, asset: Asset, page_ranges: PageRanges):
        """
        Constructs a new :samp:`ReorderPagesParams` instance.

        :param asset:  Asset to be reordered, can not be None.
        :type asset: Asset
        :param page_ranges: The page ranges to be used for reordering pages, can not be None.
        :type page_ranges: PageRanges
        :return: A new instance of ReorderPagesParams
        :rtype: ReorderPagesParams
        """
        self.__asset = asset
        self.__page_ranges = page_ranges

    def get_asset(self):
        """
        :return: Asset to be reordered.
        :rtype: Asset
        """
        return self.__asset

    def get_page_ranges(self):
        """
        :return: PageRanges to be used for reordering pages.
        :rtype: PageRanges
        """
        return self.__page_ranges
