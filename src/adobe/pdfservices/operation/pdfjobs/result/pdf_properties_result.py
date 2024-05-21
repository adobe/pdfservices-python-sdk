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

from adobe.pdfservices.operation.pdfjobs.result.pdf_services_job_result import PDFServicesJobResult


class PDFPropertiesResult(PDFServicesJobResult):
    """
    This class encapsulates the result of
    :class:`PDFPropertiesJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_properties_job.PDFPropertiesJob>`.
    """

    def __init__(self, pdf_properties_dict: str):
        """
        Constructs a new :class:`.PDFPropertiesResult` instance with PDF Properties JSON string.

        :param pdf_properties_dict: PDF Properties JSON String
        :type pdf_properties_dict: str
        """
        self._pdf_properties_dict = pdf_properties_dict

    def get_pdf_properties_dict(self):
        """
        :return: Returns PDF Properties JSON string.
        :rtype: string
        """
        return self._pdf_properties_dict
