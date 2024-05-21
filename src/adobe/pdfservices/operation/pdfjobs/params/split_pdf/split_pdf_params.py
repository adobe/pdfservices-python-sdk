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

import json
from typing import Optional

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class SplitPDFParams(PDFServicesJobParams):
    """
   Parameters for splitting a pdf using
   :class:`SplitPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.split_pdf_job.SplitPDFJob>`
   """
    json_hint = {
        'page_ranges': 'pageRanges',
        'page_count': 'pageCount',
        'file_count': 'fileCount'
    }

    @enforce_types
    def __init__(self, *,
                 page_ranges: Optional[PageRanges] = None,
                 page_count: Optional[int] = None,
                 file_count: Optional[int] = None):
        """
        Constructs a new :samp:`SplitPDFParams` instance.

        :param page_ranges: see :class:`PageRanges<adobe.pdfservices.operation.pdfjobs.params.page_ranges.PageRanges>`.
            (Optional, use key-value)
        :type page_ranges: PageRanges
        :param page_count: The page count to be used for splitting pages. (Optional, use key-value)
        :type page_count: int
        :param file_count: The file count to be used for splitting pages. (Optional, use key-value)
        :type file_count: int
        :return: A new instance of SplitPDFParams
        :rtype: SplitPDFParams
        """
        if page_ranges is not None:
            self.page_ranges = page_ranges.get_ranges()
        self.page_count = page_count
        self.file_count = file_count
        ValidationUtil.validate_split_pdf_operation_params(page_ranges, self.page_count, self.file_count)

    def get_page_ranges(self):
        """
        :return: PageRanges to be used for splitting pages.
        :rtype: PageRanges
        """
        return self.page_ranges

    def get_page_count(self):
        """
        :return: Returns the page count to be used for splitting pages.
        :rtype: int
        """
        return self.page_count

    def get_file_count(self):
        """
        :return: Returns the file count to be used for splitting pages.
        :rtype: int
        """
        return self.file_count

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
