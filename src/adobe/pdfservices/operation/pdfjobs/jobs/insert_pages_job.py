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
from adobe.pdfservices.operation.pdfjobs.params.insert_pages.insert_pages_params import InsertPagesParams
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges


class InsertPagesJob(PDFServicesJob):
    """
    A job that can be used to insert pages of multiple PDF files into a base PDF file.

    For more complex use cases, refer the
    :class:`CombinePDFJob<adobe.pdfservices.operation.pdfjobs.jobs.combine_pdf_job.CombinePDFJob>`.

    Sample Usage:

    .. code-block:: python

        base_file = open('SOURCE_PATH', 'rb')
        base_input_stream = base_file.read()
        base_file.close()
        file_to_insert = open('SOURCE_PATH_1', 'rb')
        input_stream_to_insert = file_to_insert.read()
        file_to_insert.close()
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        base_asset = pdf_services.upload(input_stream=base_input_stream,
                                         mime_type=MediaType.PDF)
        asset_to_insert = pdf_services.upload(input_stream=input_stream_to_insert,
                                      mime_type=MediaType.PDF)
        page_ranges = PageRanges().add_range(1, 3)
        insert_pages_params = InsertPagesParams(base_asset=base_asset)
        insert_pages_params.add_pages_to_insert(input_asset=asset_to_insert, page_ranges=page_ranges, base_page=2)
        insert_pages_job = InsertPagesJob(insert_pages_params=insert_pages_params)
        location = pdf_services.submit(insert_pages_job)
        pdf_services_response = pdf_services.get_job_result(location, InsertPagesResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

    """

    @enforce_types
    def __init__(self, insert_pages_params: InsertPagesParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`InsertPagesPDFJob` instance.

        :param insert_pages_params: Object containing the input files and the page numbers to insert at;
            can not be None.
        :type insert_pages_params: InsertPagesParams
        :param output_asset: Object representing the output asset. (Optional, use key-value)
            External assets can be set as output only when input is external asset as well
        :type output_asset: Asset
        """
        self.__insert_pages_params: InsertPagesParams = insert_pages_params
        self.__output_asset: Asset = output_asset
        ValidationUtil.validate_insert_asset_inputs(self.__insert_pages_params.get_base_asset(),
                                                    self.__insert_pages_params.get_assets_to_insert())

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        insert_pages_request = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                insert_pages_request,
                                                OperationHeaderInfoEndpointMap.INSERT_PAGES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.INSERT_PAGES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None) -> PDFServicesAPIRequest:
        combine_pdf_params: CombinePDFParams = self.__get_files_to_insert(self.__insert_pages_params.get_base_asset(),
                                                                          self.__insert_pages_params.get_assets_to_insert())
        insert_pages_request: PDFServicesAPIRequest

        if isinstance(self.__insert_pages_params.get_base_asset(), CloudAsset):
            insert_pages_request = CombinePDFInternalAssetRequest(combine_pdf_params,
                                                                  notify_config_list)
        else:
            insert_pages_request = CombinePDFExternalAssetRequest(combine_pdf_params,
                                                                  notify_config_list,
                                                                  self.__output_asset)
        return insert_pages_request

    @staticmethod
    def __get_files_to_insert(base_asset: Asset, files_to_insert: dict) -> CombinePDFParams:
        asset_list = []
        page_range_list = []
        base_file_start_index = 1

        for key, value in files_to_insert.items():
            if key != 1:
                asset_list.append(base_asset)
                page_range_list.append(PageRanges().add_range(base_file_start_index, key - 1))
                base_file_start_index = key
            # check for scope of typecasting/typechecking here
            for combine_pdf_job_input in value:
                asset_list.append(combine_pdf_job_input.get_asset())
                page_range_list.append(combine_pdf_job_input.get_page_ranges())

        asset_list.append(base_asset)
        page_range_list.append(PageRanges().add_all_from(base_file_start_index))

        combine_pdf_params = CombinePDFParams()

        for i in range(len(asset_list)):
            combine_pdf_params.add_asset(asset_list[i], page_ranges=page_range_list[i])

        return combine_pdf_params

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__insert_pages_params.get_base_asset(), CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
