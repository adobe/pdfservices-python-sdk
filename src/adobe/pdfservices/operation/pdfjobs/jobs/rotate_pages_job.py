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
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob
from adobe.pdfservices.operation.pdfjobs.params.rotate_pages.rotate_pages_params import RotatePagesParams


class RotatePagesJob(PDFServicesJob):
    """
    A job that allows rotation of specific pages in a PDF file.

    Sample Usage:

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
        rotate_pages_params = RotatePagesParams()
        rotate_pages_params.add_angle_to_rotate(angle=Angle.ANGLE_90)
        reorder_pages_job = RotatePagesJob(input_asset=input_asset, rotate_pages_params=rotate_pages_params)
        location = pdf_services.submit(reorder_pages_job)
        pdf_services_response = pdf_services.get_job_result(location, RotatePagesResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

    """

    @enforce_types
    def __init__(self, input_asset: Asset, rotate_pages_params: RotatePagesParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`RotatePagesJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param rotate_pages_params: RotatePagesParams} object containing the rotation angle and page ranges;
            can not be None.
        :type rotate_pages_params: RotatePagesParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        """
        self.__input_asset: Asset = input_asset
        self.__rotate_pages_params: RotatePagesParams = rotate_pages_params
        self.__output_asset: Asset = output_asset
        ValidationUtil.validate_rotate_page_actions(rotate_pages_params.get_page_actions())

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        rotate_pages_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                rotate_pages_request,
                                                OperationHeaderInfoEndpointMap.ROTATE_PAGES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.ROTATE_PAGES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        rotate_pages_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            rotate_pages_request = PageManipulationInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                        self.__get_page_action_commands(),
                                                                        notify_config_list)
        else:
            rotate_pages_request = PageManipulationExternalAssetRequest(self.__input_asset,
                                                                        self.__get_page_action_commands(),
                                                                        notify_config_list,
                                                                        self.__output_asset)

        return rotate_pages_request

    def __get_page_action_commands(self) -> PageActionCommands:
        page_action_commands = PageActionCommands()
        for rotate_page_action in self.__rotate_pages_params.get_page_actions().get_actions():
            page_action_commands.add_command(PageActionCommand.create_from(rotate_page_action))
        return page_action_commands

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
