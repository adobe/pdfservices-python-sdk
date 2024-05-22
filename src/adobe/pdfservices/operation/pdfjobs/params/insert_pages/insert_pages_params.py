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


class InsertPagesParams(PDFServicesJobParams):
    """
    Parameters for inserting pages in a PDF using
    :class:`InsertPagesJob<adobe.pdfservices.operation.pdfjobs.jobs.insert_pages_job.InsertPagesJob>`
    """

    @enforce_types
    def __init__(self, base_asset: Asset):
        """
        Constructs a new :samp:`InsertPagesParams` instance.

        :param base_asset: Base asset into which the pages are to be inserted.
        :type base_asset: Asset
        """
        self.__base_asset = base_asset
        self.__assets_to_insert = {}

    @enforce_types
    def add_pages_to_insert(self, input_asset: Asset, base_page: int, *,
                            page_ranges: PageRanges = PageRanges().add_all()):
        """
        Adds the specified pages of the input PDF file to be inserted at the specified page of the base PDF file

        This method can be invoked multiple times with the same or different input PDF files.

        All the pages of the input PDF file will be inserted at the specified page of the base PDF file if page_ranges
        is not specified.

        :param input_asset: A PDF file for insertion; can not be None.
        :type input_asset: Asset
        :param base_page: Page of the base PDF file; can not be None.
        :type base_page: int
        :param page_ranges: Page ranges of the input PDF file. (Optional, use key-value)
        :type page_ranges: PageRanges
        """
        combine_pdf_job_input = CombinePDFJobInput(input_asset, page_ranges)
        self.__update_files_to_insert(base_page, combine_pdf_job_input)
        return self

    def __update_files_to_insert(self, index: int, combine_pdf_job_input: CombinePDFJobInput):
        if index in self.__assets_to_insert:
            self.__assets_to_insert[index].append(combine_pdf_job_input)
        else:
            self.__assets_to_insert[index] = [combine_pdf_job_input]

    def get_base_asset(self):
        """
        :return: base PDF Asset to which pages will be inserted.
        :rtype: Asset
        """
        return self.__base_asset

    def get_assets_to_insert(self):
        """
        :return: Returns the mapping of base Asset's page number and Asset to be inserted along with PageRanges .
        :rtype: dict
        """
        return self.__assets_to_insert
