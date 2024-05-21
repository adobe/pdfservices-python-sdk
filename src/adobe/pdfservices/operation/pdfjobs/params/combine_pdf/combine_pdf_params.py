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
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class CombinePDFParams(PDFServicesJobParams):
    """
    Parameters for combining PDFs using
    :class:`CombinePDFJob<adobe.pdfservices.operation.pdfjobs.jobs.combine_pdf_job.CombinePDFJob>`.
    """
    def __init__(self):
        """
        Constructs a new :samp:`CombinePDFParams` instance.

        :return: A new instance of CombinePDFParams
        :rtype: CombinePDFParams
        """
        self._assets_to_combine = []

    @enforce_types
    def add_asset(self, asset: Asset, *, page_ranges: PageRanges = PageRanges().add_all()):
        """
        Adds an :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>` with
        :class:`PageRanges<adobe.pdfservices.operation.pdfjobs.params.page_ranges.PageRanges>` to combine.

        :param asset: see :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`
        :type asset: Asset
        :param page_ranges: see :class:`PageRanges<adobe.pdfservices.operation.pdfjobs.params.page_ranges.PageRanges>`
            (Optional, use key-value)
        :type page_ranges: PageRanges
        """
        self._assets_to_combine.append(CombinePDFJobInput(asset, page_ranges))
        return self

    def get_assets_to_combine(self):
        """
        :return: a list of
            :class:`CombinePDFJobInput<adobe.pdfservices.operation.internal.params.combine_pdf_job_input.CombinePDFJobInput>`
            instances.
        """

        if len(self._assets_to_combine) < 1:
            raise ValueError("No input was provided for combining files")

        for combine_pdf_job_input in self._assets_to_combine:
            ValidationUtil.validate_asset_with_page_options(combine_pdf_job_input)

        first_asset_type = self._assets_to_combine[0].get_asset().__class__
        if not all(isinstance(combine_pdf_job_input.get_asset(), first_asset_type) for combine_pdf_job_input
                   in self._assets_to_combine):
            raise ValueError("All input assets must be of the same type")

        if len([combine_pdf_job_input.get_asset() for combine_pdf_job_input in self._assets_to_combine]) > 20:
            raise ValueError("Only 20 input assets can be combined in one combine job instance")

        return self._assets_to_combine
