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

from adobe.pdfservices.operation.pdf_services_job_status import PDFServicesJobStatus


class PDFServicesJobStatusResponse:
    """
    Response object encapsulating :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`
    status and retry interval.
    """
    def __init__(self, status: str, headers: {}):
        """
        Constructs :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>` status response
        with its status, headers.

        :param status: Status of the
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
        :type status: str
        :param headers: Headers of the
            :class:`PDFServicesResponse<adobe/pdfservices/operation/pdf_services_response.PDFServicesResponse>`.
        :type headers: dict
        """
        self.__status = status
        self.__headers = headers

    def get_status(self):
        """
        :return: string representation of
            :class:`PDFServicesJobStatus<adobe.pdfservices.operation.pdf_services_job_status.PDFServicesJobStatus>`
            for the :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
        :rtype: str
        """
        return self.__status

    def get_retry_interval(self) -> int:
        """
        :return: retry interval for status polling of the
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>` in seconds.
        :rtype: int
        """
        return float(
            self.__headers.get('retry-after')) if PDFServicesJobStatus.IN_PROGRESS.get_value() == self.__status else 0
