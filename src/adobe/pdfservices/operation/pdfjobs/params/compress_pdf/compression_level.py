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

from enum import Enum


class CompressionLevel(Enum):
    """
    Supported compression levels for
    :class:`CompressPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.compress_pdf_job.CompressPDFJob>`
    """

    HIGH = "HIGH"
    """
    Reduces the file size of pdf by reducing resolution of the coloured and grayscale images above 100 dpi to 72
    dpi (dots per inch).
    This option uses JPEG medium quality compression.
    Output pdf will not contain hidden layers, document structure, metadata, javascript, user properties and print
    settings.
    """

    MEDIUM = "MEDIUM"
    """
    Reduces the file size of pdf by reducing resolution of the coloured and grayscale images above 200 dpi to 144
    dpi (dots per inch).
    This option uses JP2K medium quality compression.
    """

    LOW = "LOW"
    """
    Reduces the file size of pdf by reducing resolution of the coloured and grayscale images above 250 dpi to 200
    dpi (dots per inch).
    This option uses JP2K high quality compression.
    """

    def __init__(self, compression_level):
        """
        Constructs Compression Level from its string representation

        :param compression_level: String representation
        """
        self.compression_level = compression_level

    def get_compression_level(self):
        """
        Returns the string representation of this CompressionLevel

        :return: String representation of this CompressionLevel
        """
        return self.compression_level
