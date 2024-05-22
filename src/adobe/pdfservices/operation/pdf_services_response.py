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

from adobe.pdfservices.operation.pdf_services_job_status_response import PDFServicesJobStatusResponse


class PDFServicesResponse(PDFServicesJobStatusResponse):
    """
    Response object for :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
    """

    def __init__(self, status: str, headers: {str: str}, result):
        """
        Constructs :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>` response with
        its status, headers and result.

        :param status: Status of the
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
        :type status: str
        :param headers: Headers of the :class:`.PDFServicesResponse`.
        :type headers: dict
        :param result:  result for the :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`,
            it will be an extension
            of :class:`PDFServicesJobResult<adobe.pdfservices.operation.pdfjobs.result.pdf_services_job_result.PDFServicesJobResult>`.
        """
        super().__init__(status, headers)
        self.__result = result

    def get_result(self):
        """
        :return: Returns instance of result of
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
        """
        return self.__result
