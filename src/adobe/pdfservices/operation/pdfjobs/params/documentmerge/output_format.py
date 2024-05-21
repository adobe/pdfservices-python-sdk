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


class OutputFormat(Enum):
    """
    Supported output formats for :class:`adobe.pdfservices.operation.pdfjobs.jobs.document_merge_job.py`
    """

    DOCX = "docx"
    """
    Represents "application/vnd.openxmlformats-officedocument.wordprocessingml.document" media type
    """

    PDF = "pdf"
    """
    Represents "application/pdf" media type
    """

    def __init__(self, output_format):
        """
        Constructs output format with its string representation

        :param output_format: String representation
        """
        self.__format: str = output_format

    def get_format(self):
        """
        :return: String representation of this outputformat
        """
        return self.__format
