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
from adobe.pdfservices.operation.internal.api.dto.request.createpdf.create_pdf_external_asset_request import \
    CreatePDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.createpdf.create_pdf_internal_asset_request import \
    CreatePDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.create_pdf.CreatePDFParams import CreatePDFParams


class CreatePDFJob(PDFServicesJob):
    """
    A job that converts a non-PDF file to a PDF file. Some source formats may have associated conversion parameters.

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
        input_asset = pdf_services.upload(input_stream=input_stream, mime_type=MediaType.DOCX)
        create_pdf_job = CreatePDFJob(input_asset)
        location = pdf_services.submit(create_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, CreatePDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, input_asset: Asset, *,
                 create_pdf_params: Optional[CreatePDFParams] = None,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new instance of :samp:`CreatePDFJob`.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param create_pdf_params: `CreatePDFParams` to set.(Optional, use key-value)
        :type create_pdf_params: CreatePDFParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of CreatePDFJob.
        :rtype: CreatePDFJob
        """
        self.__input_asset: Asset = input_asset
        self.__create_pdf_params: CreatePDFParams = create_pdf_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        create_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                create_pdf_request,
                                                OperationHeaderInfoEndpointMap.CREATE_PDF.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.CREATE_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        create_pdf_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            create_pdf_request = CreatePDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                               self.__create_pdf_params, notify_config_list)
        else:
            create_pdf_request = CreatePDFExternalAssetRequest(self.__input_asset, self.__create_pdf_params,
                                                               notify_config_list,
                                                               self.__output_asset)

        return create_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
