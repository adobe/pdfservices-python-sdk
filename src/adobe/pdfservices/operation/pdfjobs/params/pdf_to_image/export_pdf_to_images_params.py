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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_output_type import \
    ExportPDFToImagesOutputType
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_target_format import \
    ExportPDFToImagesTargetFormat


class ExportPDFtoImagesParams(PDFServicesJobParams):
    """
    Parameters for exporting a source PDF file to images using
    :class:`ExportPDFToImagesJob<adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_to_images_job.ExportPDFToImagesJob>`.
    """

    @enforce_types
    def __init__(self,
                 export_pdf_to_images_target_format: ExportPDFToImagesTargetFormat,
                 export_pdf_to_images_output_type: ExportPDFToImagesOutputType):
        """
        Constructs a new :samp:`ExportPDFtoImagesParams` instance.

        :param export_pdf_to_images_target_format: ExportPDFToImagesTargetFormat to which the source PDF file will be exported, can not be None.
        :type export_pdf_to_images_target_format: ExportPDFToImagesTargetFormat
        :param export_pdf_to_images_output_type: ExportPDFToImagesOutputType to be used for Export PDF to Images, can not be None.
        :type export_pdf_to_images_output_type: ExportPDFToImagesOutputType
        """
        self.__export_pdf_to_images_output_type = export_pdf_to_images_output_type
        self.__export_pdf_to_images_target_format = export_pdf_to_images_target_format

    def get_export_pdf_to_images_output_type(self):
        """
        :return: ExportPDFToImagesOutputType to be used for Export PDF to Images.
        :rtype: ExportPDFToImagesOutputType
        """
        return self.__export_pdf_to_images_output_type

    def get_export_pdf_to_images_target_format(self):
        """
        :return: ExportPDFToImagesTargetFormat to which the source PDF file will be exported.
        :rtype: ExportPDFToImagesTargetFormat
        """
        return self.__export_pdf_to_images_target_format
