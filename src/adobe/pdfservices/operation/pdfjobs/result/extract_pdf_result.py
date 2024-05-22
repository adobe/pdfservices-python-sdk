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


class ExtractPDFResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`ExtractPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job.ExtractPDFJob>`.
    """

    def __init__(self, content: Asset, resource: Asset, content_json: {}):
        """
        Constructs a new :samp:`ExtractPDFResult` instance with result content asset, resource asset and resource JSON
        object

        :param content: result content asset
        :type content: Asset
        :param resource: result resource asset
        :type resource: Asset
        :param content_json: result content json
        :type content_json: dict
        """
        self._content = content
        self._resource = resource
        self._content_json = content_json

    def get_content(self):
        """
        :return: Returns the content asset containing extracted content of PDF file, if an internal asset was used as
            input PDF.
        :rtype: Asset
        """
        return self._content

    def get_resource(self):
        """
        :return: Returns the Asset of zip file containing generated resources from extract operation.
        :rtype: Asset
        """
        return self._resource

    def get_content_json(self):
        """
        :return: Returns the content json dictionary containing extracted content of PDF file, if an internal asset
            was used as input PDF.
        :rtype: dict
        """
        return self._content_json
