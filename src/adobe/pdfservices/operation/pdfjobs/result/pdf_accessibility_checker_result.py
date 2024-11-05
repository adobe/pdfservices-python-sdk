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


class PDFAccessibilityCheckerResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`PDFAccessibilityCheckerJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_accessibility_checker_job.PDFAccessibilityCheckerJob>`.
    """

    def __init__(self, asset: Asset, report: Asset):
        """
        Constructs a new :samp:`PDFAccessibilityCheckerResult` instance

        :param asset: result asset, enclosing zipped output result
        :type asset: Asset
        :param report: result asset, enclosing zipped output result
        :type asset: Asset
       """

        self.__asset = asset
        self.__report = report

    def get_asset(self):
        """
        :return: The zipped asset associated with the PDFAccessibilityCheckerJob result, if an external asset was used as input PDF.
        :rtype: Asset
        """
        return self.__asset

    def get_report(self):
        """
        :return: The report contains links to documentation that assist in manually fixing problems using Adobe Acrobat Pro.
        :rtype: Asset
        """
        return self.__report
