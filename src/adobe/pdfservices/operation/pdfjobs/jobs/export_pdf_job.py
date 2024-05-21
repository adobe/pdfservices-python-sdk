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

import uuid
from typing import List, Optional

from adobe.pdfservices.operation.config.notifier.notifier_config import NotifierConfig
from adobe.pdfservices.operation.internal.api.dto.request.exportpdf.export_pdf_external_asset_request import \
    ExportPDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.exportpdf.export_pdf_internal_asset_request import \
    ExportPDFInternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.constants.operation_header_info_endpoint_map import \
    OperationHeaderInfoEndpointMap
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.pdf_services_helper import PDFServicesHelper
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams


class ExportPDFJob(PDFServicesJob):
    """
    A job which exports a source PDF file to a supported format specified by
    :class:`ExportPDFTargetFormat<adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format.ExportPDFTargetFormat>`

    For example, a PDF can be exported to a DOCX file as follows:

    Sample usage.

    .. code-block:: python

        file = open('SOURCE_PATH', 'rb')
        input_stream = file.read()
        file.close()
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        input_asset = pdf_services.upload(input_stream=input_stream, mime_type=MediaType.PDF)
        export_pdf_params = ExportPDFParams(target_format=ExportPDFTargetFormat.DOCX)
        export_pdf_job = ExportPDFJob(input_asset=input_asset, export_pdf_params=export_pdf_params)
        location = pdf_services.submit(export_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, ExportPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

    """

    @enforce_types
    def __init__(self, input_asset: Asset, export_pdf_params: ExportPDFParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`ExportPDFJob` instance.

        :param input_asset: Asset object containing the input file; can not be None.
        :type input_asset: Asset
        :param export_pdf_params: ExportPDFParams object containing the export parameters; can not be None.
        :type export_pdf_params: ExportPDFParams
        :param output_asset: Asset object representing the output asset. (Optional, use key-value)
        :type output_asset: Asset
        :return: A new instance of ExportPDFJob.
        :rtype: ExportPDFJob
        .. note::
            External assets can be set as output only when input is external asset as well
        """
        self.__input_asset: Asset = input_asset
        self.__export_pdf_params: ExportPDFParams = export_pdf_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        export_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                export_pdf_request,
                                                OperationHeaderInfoEndpointMap.EXPORT_PDF.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.EXPORT_PDF_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        export_pdf_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            export_pdf_request = ExportPDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                               self.__export_pdf_params, notify_config_list)
        else:
            export_pdf_request = ExportPDFExternalAssetRequest(self.__input_asset, self.__export_pdf_params,
                                                               notify_config_list,
                                                               self.__output_asset)

        return export_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
