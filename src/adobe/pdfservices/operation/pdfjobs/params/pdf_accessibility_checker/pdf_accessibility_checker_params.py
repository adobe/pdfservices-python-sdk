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

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class PDFAccessibilityCheckerParams(PDFServicesJobParams):
    """
    Parameters for Accessibility Checker PDFs using
    :class:`PDFAccessibilityCheckerJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_accessibility_checker_job.PDFAccessibilityCheckerJob>`.
    """

    @enforce_types
    def __init__(self, *, page_start: Optional[int] = None,
                 page_end: Optional[int] = None):
        """
        Constructs a new :samp:`PDFAccessibilityCheckerParams` instance.

        :param page_start: The start page number.
        :type page_start: int
        :param page_end: The end page number.
        :type page_end: int
        """
        if page_start is not None and page_start < 1:
            raise SdkException("Page start should be greater than 0")
        if page_end is not None and page_end < 1:
            raise SdkException("Page end should be greater than 0")
        self.__page_start = page_start
        self.__page_end = page_end

    def get_page_start(self):
        """
        :return: return the start page number.
        :rtype: int
        """
        return self.__page_start

    def get_page_end(self):
        """
        :return: return the end page number.
        :rtype: int
        """
        return self.__page_end
