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


class ExportPDFToImagesTargetFormat(Enum):
    """
    Supported target formats for :class:`ExportPDFToImagesJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_to_images_job.ExportPDFToImagesJob>`.
    """

    JPEG = "jpeg"
    """
    Represents "image/jpeg" media type.
    """

    PNG = "png"
    """
    Represents "image/png" media type.
    """

    def __init__(self, file_ext):
        self.file_ext = file_ext

    def get_file_ext(self):
        """
        :return: file extension of this format.
        """
        return self.file_ext
