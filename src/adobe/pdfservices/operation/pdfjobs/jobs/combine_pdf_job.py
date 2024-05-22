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
from adobe.pdfservices.operation.internal.api.dto.request.combinepdf.combine_pdf_external_asset_request import \
    CombinePDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.combinepdf.combine_pdf_internal_asset_request import \
    CombinePDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.combine_pdf.combine_pdf_params import CombinePDFParams


class CombinePDFJob(PDFServicesJob):
    """
    A job that combines multiple PDF files into a single PDF file. Allows specifying which pages of the source
    files to combine.

    Sample usage.

    .. code-block:: python

        file = open('SOURCE_PATH_1', 'rb')
        input_stream_1 = file.read()
        file.close()
        file = open('SOURCE_PATH_2', 'rb')
        input_stream_2 = file.read()
        file.close()
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        stream_assets = [StreamAsset(input_stream_1, MediaType.PDF),
                         StreamAsset(input_stream_2, MediaType.PDF)]
        assets = pdf_services.upload_assets(stream_assets)
        combine_pdf_params = ((CombinePDFParams()
                              .add_asset(assets[0]))
                              .add_asset(assets[1]))
        combine_pdf_job = CombinePDFJob(combine_pdf_params=combine_pdf_params)
        location = pdf_services.submit(combine_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, CombinePDFResult)
        result_asset: CombinePDFResult = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, combine_pdf_params: CombinePDFParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`CombinePDFJob` instance.

        :param combine_pdf_params: `CombinePDFParams` to set; can not be None.
        :type combine_pdf_params: CombinePDFParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of CombinePDFJob
        :rtype: CombinePDFJob
        """
        self.__combine_pdf_params: CombinePDFParams = combine_pdf_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        combine_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                combine_pdf_request,
                                                OperationHeaderInfoEndpointMap.COMBINE_PDF.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.COMBINE_PDF_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        combine_pdf_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__combine_pdf_params.get_assets_to_combine()[0].get_asset(), CloudAsset):
            combine_pdf_request = CombinePDFInternalAssetRequest(self.__combine_pdf_params, notify_config_list)
        else:
            combine_pdf_request = CombinePDFExternalAssetRequest(self.__combine_pdf_params,
                                                                 notify_config_list,
                                                                 self.__output_asset)

        return combine_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if (self.__output_asset is not None and
                isinstance(self.__combine_pdf_params.get_assets_to_combine()[0].get_asset(), CloudAsset)):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
