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
from adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compression_level import CompressionLevel
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class CompressPDFParams(PDFServicesJobParams):
    """
    Parameters for reducing file size of a pdf using
    :class:`CompressPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.compress_pdf_job.CompressPDFJob>`
    """

    @enforce_types
    def __init__(self, *, compression_level: CompressionLevel = CompressionLevel.MEDIUM):
        """
        Creates an instance of :samp:`CompressPDFParams`

        :param compression_level: see :class:`CompressionLevel<adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compression_level.CompressionLevel>`. (Optional, use key-value)
        :type compression_level: CompressionLevel
        """
        self.__compression_level = compression_level

    def get_compression_level(self):
        """ Returns the compression level to be used for Compress PDF, specified by
        :class:`CompressionLevel<adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compression_level.CompressionLevel>`
        """
        return self.__compression_level
