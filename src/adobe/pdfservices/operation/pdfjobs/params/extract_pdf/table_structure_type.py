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


class TableStructureType(Enum):
    """
    Supported Formats for exporting Table Data :class:`ExtractPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job.ExtractPDFJob>`.
    """

    CSV = "csv"
    """
    CSV Format
    """

    XLSX = "xlsx"
    """
    XLSX Format
    """

    def __str__(self):
        return self.value
