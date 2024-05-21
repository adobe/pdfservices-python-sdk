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

from adobe.pdfservices.operation.pdfjobs.result.pdf_services_job_result import PDFServicesJobResult


class ExportPDFtoImagesResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`ExportPDFToImagesJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_to_images_job.ExportPDFToImagesJob>`.
    """

    def __init__(self, assets: []):
        """
        Constructs a new :samp:`ExportPDFToImagesResult` instance

        :param assets: List of result assets
        :type assets: list
        """
        self._assets = assets

    def get_assets(self):
        """
        :return: the list of result assets
        :rtype: Asset
        """
        return self._assets
