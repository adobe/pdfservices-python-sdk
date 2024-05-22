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


class AutotagPDFResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`AutotagPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.autotag_pdf_job.AutotagPDFJob>`.
    """
    def __init__(self, tagged_pdf: Asset, report: Asset, resource: Asset):
        """
        Constructs a new :samp:`AutotagPDFResult` instance with the tagged PDF asset and report asset.

        :param tagged_pdf: tagged PDF asset
        :type tagged_pdf: Asset
        :param report: report asset
        :type report: Asset
        :param resource: resource asset
        :type resource: Asset
        """
        self._tagged_pdf = tagged_pdf
        self._report = report
        self._resource = resource

    def get_tagged_pdf(self):
        """
        :return: Returns tagged PDF asset, if an internal asset was used as input PDF.
        :rtype: Asset
        """
        return self._tagged_pdf

    def get_report(self):
        """
        :return: Returns report asset, if an internal asset was used as input PDF.
        :rtype: Asset
        """
        return self._report

    def get_resource(self):
        """
        :return: The zipped asset associated with the
            :class:`AutotagPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.autotag_pdf_job.AutotagPDFJob>` result,
            if an external asset was used as input PDF.
        :rtype: Asset
        """
        return self._resource
