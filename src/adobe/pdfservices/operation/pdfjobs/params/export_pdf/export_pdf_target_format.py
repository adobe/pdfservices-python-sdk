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


class ExportPDFTargetFormat(Enum):
    """
    Supported target formats for
    :class:`ExportPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job.ExportPDFJob>`
    """


    DOC = "doc"
    """
    Represents "application/msword" media type
    """

    DOCX = "docx"
    """
    Represents "application/vnd.openxmlformats-officedocument.wordprocessingml.document" media type
    """

    PPTX = "pptx"
    """
    Represents "application/vnd.openxmlformats-officedocument.presentationml.presentation" media type
    """

    RTF = "rtf"
    """
    Represents "text/rtf" media type
    """

    XLSX = "xlsx"
    """
    Represents "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" media type
    """
    def __init__(self, file_ext):
        """
        Constructor.

        :param file_ext: file extension
        """
        self.file_ext = file_ext

    def get_file_ext(self):
        """
        Returns the file extension of this format.

        :return: file extension of this format
        """
        return self.file_ext
