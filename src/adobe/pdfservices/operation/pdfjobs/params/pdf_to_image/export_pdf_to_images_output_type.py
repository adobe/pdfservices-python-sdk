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


class ExportPDFToImagesOutputType(Enum):
    """
    List of supported outputTypes for :class:`ExportPDFToImagesJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_to_images_job.ExportPDFToImagesJob>`.
    """

    LIST_OF_PAGE_IMAGES = "listOfPageImages"
    """
    Represents List Output type.
    """

    ZIP_OF_PAGE_IMAGES = "zipOfPageImages"
    """
    Represents Zip Output type.
    """

    def __init__(self, output_type):
        self.output_type = output_type

    def get_output_type(self):
        """
        :return: output type.
        """
        return self.output_type
