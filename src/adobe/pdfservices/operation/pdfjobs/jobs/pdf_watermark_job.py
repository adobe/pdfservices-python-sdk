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
from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.api.dto.request.pdfwatermark.pdf_watermark_external_asset_request import \
    PDFWatermarkExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pdfwatermark.pdf_watermark_internal_asset_request import \
    PDFWatermarkInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.pdf_watermark.pdf_watermark_params import PDFWatermarkParams


class PDFWatermarkJob(PDFServicesJob):
    """
    PDF Watermark API will add a watermark on specified pages of PDF document using a source watermark PDF.
    The first page of source watermark PDF will be added as a watermark in input PDF document.

    Sample usage.

    .. code-block:: python

        pdf_file = open('SOURCE_PATH', 'rb')
        input_stream = pdf_file.read()
        pdf_file.close()

        pdf_file = open('SOURCE_PATH', 'rb')
        watermark_asset = pdf_file.read()
        watermark_asset.close()

        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)
        watermark_asset = pdf_services.upload(input_stream=watermark_asset, mime_type=PDFServicesMediaType.PDF)

        watermark_appearance = WatermarkAppearance(appear_on_foreground=True, opacity=100)

        page_ranges = PageRanges()
        page_ranges.add_range(1, 4)
        # Create parameters for the job
        pdf_watermark_params = PDFWatermarkParams(page_ranges=page_ranges, watermark_appearance=watermark_appearance)

        # Creates a new job instance
        pdf_watermark_job = PDFWatermarkJob(input_asset=input_asset, watermark_asset=watermark_asset,
                                     pdf_watermark_params=pdf_watermark_params)
        location = pdf_services.submit(pdf_watermark_job)
        pdf_services_response = pdf_services.get_job_result(location, PDFWatermarkResult)
        pdf_watermark_result: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(pdf_watermark_result)

    """

    @enforce_types
    def __init__(self, input_asset: Asset, watermark_asset: Asset, *,
                 pdf_watermark_params: Optional[PDFWatermarkParams] = None, output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`PDFWatermarkJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param watermark_asset: The watermark asset for the job; can not be None.
        :type watermark_asset: Asset
        :param pdf_watermark_params: Parameters for water mark (Optional, use key-value)
        :type pdf_watermark_params: PDFWatermarkParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of PDFWatermarkJob.
        :rtype: PDFWatermarkJob
        """

        self.__input_asset = input_asset
        self.__watermark_asset = watermark_asset
        self.__pdf_watermark_params = pdf_watermark_params
        self.__output_asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)

        pdf_watermark_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context, pdf_watermark_request,
                                                OperationHeaderInfoEndpointMap.PDF_WATERMARK.get_endpoint(),
                                                x_request_id, ServiceConstants.PDF_WATERMARK_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        pdf_watermark_request: PDFServicesAPIRequest
        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):

            watermark_asset_id = self.__watermark_asset.get_asset_id() if self.__watermark_asset is not None else None
            pdf_watermark_request = PDFWatermarkInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                     watermark_asset_id,
                                                                     self.__pdf_watermark_params, notify_config_list)
        else:
            pdf_watermark_request = PDFWatermarkExternalAssetRequest(self.__input_asset, self.__watermark_asset,
                                                                     self.__pdf_watermark_params, notify_config_list,
                                                                     self.__output_asset)

        return pdf_watermark_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)

        if self.__input_asset is None:
            raise SdkException("Input asset cannot be None")
        if self.__watermark_asset is None:
            raise SdkException("Watermark asset cannot be None")

        if self.__watermark_asset is not None and not isinstance(self.__watermark_asset,
                                                                 self.__input_asset.__class__):
            raise SdkException("Input asset and Watermark Image Asset must be of same type")
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
