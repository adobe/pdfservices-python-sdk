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
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.delete_page_action import \
    DeletePageAction
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action_command import \
    PageActionCommand
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action_commands import \
    PageActionCommands
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_manipulation_external_asset_request import \
    PageManipulationExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_manipulation_internal_asset_request import \
    PageManipulationInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.delete_pages.delete_pages_params import DeletePagesParams


class DeletePagesJob(PDFServicesJob):
    """
    A job to delete pages in a PDF file.

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
        input_asset = pdf_services.upload(input_stream=input_stream,
                                          mime_type=MediaType.PDF)
        page_ranges_for_deletion = PageRanges()
        page_ranges.add_single_page(1)
        delete_pages_params = DeletePagesParams(page_ranges=page_ranges_for_deletion)
        delete_pages_job = DeletePagesJob(input_asset=input_asset,
                                          delete_pages_params=delete_pages_params)
        location = pdf_services.submit(delete_pages_job)
        pdf_services_response = pdf_services.get_job_result(location, CompressPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """
    @enforce_types
    def __init__(self, input_asset: Asset, delete_pages_params: DeletePagesParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`DeletePagesJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param delete_pages_params: DeletePagesParams to set.(Optional, use key-value)
        :type delete_pages_params: DeletePagesParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of DeletePagesJob
        :rtype: DeletePagesJob
        """
        self.__input_asset: Asset = input_asset
        self.__delete_pages_params: DeletePagesParams = delete_pages_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        delete_pages_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                delete_pages_request,
                                                OperationHeaderInfoEndpointMap.DELETE_PAGES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.DELETE_PAGES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        delete_pages_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            delete_pages_request = PageManipulationInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                        self.__get_page_action_commands(),
                                                                        notify_config_list)
        else:
            delete_pages_request = PageManipulationExternalAssetRequest(self.__input_asset,
                                                                        self.__get_page_action_commands(),
                                                                        notify_config_list,
                                                                        self.__output_asset)

        return delete_pages_request

    def __get_page_action_commands(self) -> PageActionCommands:
        page_action_commands = PageActionCommands()
        delete_action = DeletePageAction(self.__delete_pages_params.get_page_ranges())
        page_action_commands.add_command(PageActionCommand.create_from(delete_action))
        return page_action_commands

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
