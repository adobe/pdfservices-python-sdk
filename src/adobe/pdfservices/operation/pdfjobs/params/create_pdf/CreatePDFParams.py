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

from abc import abstractmethod, ABC

from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class CreatePDFParams(PDFServicesJobParams, ABC):
    """
    Marker base class for :class:`CreatePDFJob<adobe.pdfservices.operation.pdfjobs.jobs.create_pdf_job.CreatePDFJob>`
    params. The factory methods within this class can be used to create instances of params classes corresponding to
    the source media type.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_create_tagged_pdf(self):
        pass

    @abstractmethod
    def get_document_language(self):
        pass
