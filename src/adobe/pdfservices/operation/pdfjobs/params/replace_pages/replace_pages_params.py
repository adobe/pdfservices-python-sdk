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

from adobe.pdfservices.operation.internal.params.combine_pdf_job_input import CombinePDFJobInput
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class ReplacePagesParams(PDFServicesJobParams):
    """
    Parameters for replacing pages of a pdf using
    :class:`ReplacePagesJob<adobe.pdfservices.operation.pdfjobs.jobs.replace_pages_job.ReplacePagesJob>`
    """

    @enforce_types
    def __init__(self, base_asset: Asset):
        """
        Constructs a new :samp:`ReplacePagesParams` instance.

        :param base_asset: The base asset to be used for replacing pages, can not be None.
        :type base_asset: Asset
        :return: A new instance of ReplacePagesParams
        :rtype: ReplacePagesParams
        """
        self.__base_asset = base_asset
        self.__assets_to_replace = {}

    @enforce_types
    def add_pages_to_replace(self, input_asset: Asset, base_page: int, *,
                             page_ranges: PageRanges = PageRanges().add_all()):
        """
        :param input_asset: a PDF file for insertion
        :type input_asset: Asset
        :param page_ranges: page ranges of the input PDF file
        :type page_ranges: PageRanges
        :param base_page: page of the base PDF file
        :type base_page: int
        """
        combine_pdf_job_input = CombinePDFJobInput(input_asset, page_ranges)
        self.__assets_to_replace[base_page] = combine_pdf_job_input
        return self

    def get_base_asset(self):
        """
        :return: Returns the base PDF Asset to which pages will be replaced.
        :rtype: Asset
        """
        return self.__base_asset

    def get_assets_to_replace(self):
        """
        :return: Returns the mapping of base Asset's page number and Asset to be replaced along
            with PageRanges.
        """
        return self.__assets_to_replace
