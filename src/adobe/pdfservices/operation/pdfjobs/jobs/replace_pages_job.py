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
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob
from adobe.pdfservices.operation.pdfjobs.params.combine_pdf.combine_pdf_params import CombinePDFParams
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.replace_pages.replace_pages_params import ReplacePagesParams


class ReplacePagesJob(PDFServicesJob):
    """
    A job that allows specific pages in a PDF file to be replaced with pages from multiple PDF files.

    Sample usage.

    .. code-block:: python

        base_file = open('SOURCE_PATH', 'rb')
        base_input_stream = base_file.read()
        base_file.close()
        file_1 = open('SOURCE_PATH', 'rb')
        input_stream_1 = file_1.read()
        file_1.close()
        file_2 = open('SOURCE_PATH', 'rb')
        input_stream_2 = file_2.read()
        file_2.close()
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        base_asset = pdf_services.upload(input_stream=base_input_stream,
                                          mime_type=MediaType.PDF)
        asset_1 = pdf_services.upload(input_stream=input_stream_1,
                                     mime_type=MediaType.PDF)
        asset_2 = pdf_services.upload(input_stream=input_stream_2,
                                      mime_type=MediaType.PDF)
        page_ranges = PageRanges().add_range(3, 4)
                            .add_single_page(1)
        replace_pages_params = ReplacePagesParams(base_asset=base_asset)
        replace_pages_params.add_pages_to_replace(input_asset=asset_1, page_ranges=page_ranges, base_page=1)
        replace_pages_params.add_pages_to_replace(input_asset=asset_2, base_page=3)
        replace_pages_job = ReplacePagesJob(replace_pages_params=replace_pages_params)
        location = pdf_services.submit(replace_pages_job)
        pdf_services_response = pdf_services.get_job_result(location, ReplacePagesResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, replace_pages_params: ReplacePagesParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`ReplacePagesJob` instance.

        :param replace_pages_params: `ReplacePagesParams` to set; can not be None.
        :type replace_pages_params: ReplacePagesParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of `ReplacePagesJob`.
        :rtype: ReplacePagesJob
        """
        self.__replace_pages_params: ReplacePagesParams = replace_pages_params
        self.__output_asset: Asset = output_asset
        ValidationUtil.validate_replace_files_inputs(self.__replace_pages_params.get_base_asset(),
                                                     self.__replace_pages_params.get_assets_to_replace())

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        replace_pages_request = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                replace_pages_request,
                                                OperationHeaderInfoEndpointMap.REPLACE_PAGES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.REPLACE_PAGES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None) -> PDFServicesAPIRequest:
        combine_pdf_params: CombinePDFParams = self.__get_files_to_replace(self.__replace_pages_params.get_base_asset(),
                                                                           self.__replace_pages_params.get_assets_to_replace())
        replace_pages_request: PDFServicesAPIRequest

        if isinstance(self.__replace_pages_params.get_base_asset(), CloudAsset):
            replace_pages_request = CombinePDFInternalAssetRequest(combine_pdf_params,
                                                                   notify_config_list)
        else:
            replace_pages_request = CombinePDFExternalAssetRequest(combine_pdf_params,
                                                                   notify_config_list,
                                                                   self.__output_asset)
        return replace_pages_request

    @staticmethod
    def __get_files_to_replace(base_asset: Asset, files_to_replace: dict) -> CombinePDFParams:

        asset_list = []
        page_range_list = []
        base_file_start_index = 1

        for key, value in files_to_replace.items():
            if key != base_file_start_index:
                asset_list.append(base_asset)
                page_range_list.append(PageRanges().add_range(base_file_start_index, key - 1))
            # check for scope of typecasting/typechecking here

            asset_list.append(value.get_asset())
            page_range_list.append(value.get_page_ranges())
            base_file_start_index = key + 1

        asset_list.append(base_asset)
        page_range_list.append(PageRanges().add_all_from(base_file_start_index))

        combine_pdf_params = CombinePDFParams()

        for i in range(len(asset_list)):
            combine_pdf_params.add_asset(asset_list[i], page_ranges=page_range_list[i])

        return combine_pdf_params

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__replace_pages_params.get_base_asset(), CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
