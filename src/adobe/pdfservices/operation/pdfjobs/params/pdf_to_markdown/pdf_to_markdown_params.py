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
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class PDFToMarkdownParams(PDFServicesJobParams):
    """
    Parameters for controlling the PDF to Markdown conversion process.
    """

    @enforce_types
    def __init__(self, *, get_figures: bool = False):
        """
        Constructs a new instance of :samp:`PDFToMarkdownParams`.

        :param get_figures: Whether to extract figures from the PDF. (Optional, use key-value)
        :type get_figures: bool
        :return: A new instance of PDFToMarkdownParams.
        :rtype: PDFToMarkdownParams
        """
        super().__init__()
        self.__get_figures: bool = get_figures

    def get_figures(self) -> bool:
        """
        Returns whether figures should be extracted from the PDF.

        :return: True if figures should be extracted, False otherwise.
        :rtype: bool
        """
        return self.__get_figures

