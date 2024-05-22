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
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.api.dto.request.splitpdf.split_pdf_external_asset_request import \
    SplitPDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.splitpdf.split_pdf_internal_asset_request import \
    SplitPDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.split_pdf.split_pdf_params import SplitPDFParams


class SplitPDFJob(PDFServicesJob):
    """
    A job that splits PDF document into multiple smaller documents by simply specifying either the number of files,
    pages per file, or page ranges.

    Sample usage.

    .. code-block:: python

        file = open('SOURCE_PATH', 'rb')
        base_input_stream = base_file.read()
        file.close()
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        input_asset = pdf_services.upload(input_stream=input_stream, mime_type=MediaType.PDF)
        split_pdf_params = SplitPDFParams(page_count=2)
        split_pdf_job = SplitPDFJob(input_asset, split_pdf_params)
        location = pdf_services.submit(split_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, SplitPDFResult)
        result_assets = pdf_services_response.get_result().get_assets()
    """

    @enforce_types
    def __init__(self, input_asset: Asset, split_pdf_params: SplitPDFParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`SplitPDFJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param split_pdf_params: `SplitPDFParams` to set; can not be None.
        :type split_pdf_params: SplitPDFParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of `SplitPDFJob`.
        :rtype: SplitPDFJob
        """
        self.__input_asset: Asset = input_asset
        self.__split_pdf_params: SplitPDFParams = split_pdf_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        self._validate(execution_context)
        split_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid4())

        response = PDFServicesHelper.submit_job(execution_context,
                                                split_pdf_request,
                                                OperationHeaderInfoEndpointMap.SPLIT_PDF.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.SPLIT_PDF_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        split_pdf_request: PDFServicesAPIRequest

        if isinstance(self.__input_asset, CloudAsset):
            split_pdf_request = SplitPDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                             self.__split_pdf_params, notify_config_list)

        else:
            split_pdf_request = SplitPDFExternalAssetRequest(self.__input_asset,
                                                             self.__split_pdf_params, notify_config_list,
                                                             self.__output_asset)

        return split_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
