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
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class DeletePagesParams(PDFServicesJobParams):
    """
    Parameters for deleting pages from a pdf using
    :class:`DeletePagesJob<adobe.pdfservices.operation.pdfjobs.jobs.delete_pages_job.DeletePagesJob>`
    """

    @enforce_types
    def __init__(self, page_ranges: PageRanges):
        """
        Creates an instance of `DeletePagesParams` with given PageRanges.

        :param page_ranges: the PageRanges to be used for deleting pages; can not be None.
        :type page_ranges: PageRanges
        """
        ValidationUtil.validate_page_ranges(page_ranges)

        self.__page_ranges = page_ranges

    def get_page_ranges(self):
        """
        :return: the PageRanges to be used for deleting pages.
        :rtype: PageRanges
        """
        return self.__page_ranges
