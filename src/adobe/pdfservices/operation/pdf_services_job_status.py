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


class PDFServicesJobStatus(Enum):
    """
    Status types for :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
    """

    IN_PROGRESS = "in progress"
    """
    Represents in progress status
    """

    FAILED = "failed"
    """
    Represents failed status
    """

    DONE = "done"
    """
    Represents completed status
    """

    def __init__(self, value: str):
        """
        Constructs PDF Services job status using its string representation.

        :param value: string representation of PDF services job status.
        :type value: str
        """
        self.__value = value

    def get_value(self):
        """
        :return: string representation of :class:`.PDFServicesJobStatus`.
        :rtype: str
        """
        return self.__value
