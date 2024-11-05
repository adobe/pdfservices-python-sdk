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

from typing import Optional
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams
from adobe.pdfservices.operation.pdfjobs.params.pdf_watermark.watermark_appearance import WatermarkAppearance


class PDFWatermarkParams(PDFServicesJobParams):
    """
    Parameters to Watermark pdf using
    :class:`PDFWatermarkJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_watermark_job.PDFWatermarkJob>`.
    """

    @enforce_types
    def __init__(self, *, page_ranges: Optional[PageRanges] = None,
                 watermark_appearance: Optional[WatermarkAppearance] = WatermarkAppearance):
        """
        Constructs a new :samp:`PDFWatermarkParams` instance.

        :param page_ranges: see :class:`PageRanges<adobe.pdfservices.operation.pdfjobs.params.page_ranges.PageRanges>`.
            (Optional, use key-value)
        :type page_ranges: PageRanges
        :param WatermarkAppearance: WatermarkAppearance; Specifies the appearance parameters for watermark
            (Optional, use key-value)
        :type WatermarkAppearance: WatermarkAppearance
        :return: A new instance of PDFWatermarkParams
        :rtype: PDFWatermarkParams
        """

        self._page_ranges = page_ranges
        self._watermark_appearance = watermark_appearance

    def get_page_ranges(self):
        """
        :return: Specifies the page ranges on which watermark has to be applied in the input PDF file.
        :rtype: PageRanges
        """
        return self._page_ranges

    def get_watermark_appearance(self):
        """
        :param WatermarkAppearance: WatermarkAppearance; Specifies the appearance parameters for watermark
            (Optional, use key-value)
        :type WatermarkAppearance: WatermarkAppearance
        """
        return self._watermark_appearance
