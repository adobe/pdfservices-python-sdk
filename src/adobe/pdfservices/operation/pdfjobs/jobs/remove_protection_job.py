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
from adobe.pdfservices.operation.internal.api.dto.request.remove_protection.remove_protection_extenal_asset_request import \
    RemoveProtectionExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.remove_protection.remove_protection_internal_asset_request import \
    RemoveProtectionInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.remove_protection.remove_protection_params import \
    RemoveProtectionParams


class RemoveProtectionJob(PDFServicesJob):
    """
    A job that allows to remove password security from a PDF document.

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
        remove_protection_params = RemoveProtectionParams(password="password")
        remove_protection_job = RemoveProtectionJob(input_asset=input_asset,
                                                    remove_protection_params=remove_protection_params)
        location = pdf_services.submit(remove_protection_job)
        pdf_services_response = pdf_services.get_job_result(location, RemoveProtectionResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, input_asset: Asset, remove_protection_params: RemoveProtectionParams,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`RemoveProtectionJob` instance.

        :param input_asset: The input asset for the job. (Mandatory, use key-value)
        :type input_asset: Asset
        :param remove_protection_params: `RemoveProtectionParams` to set; can not be None.
        :type remove_protection_params: RemoveProtectionParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of `RemoveProtectionJob`.
        :rtype: RemoveProtectionJob
        """
        self.__input_asset: Asset = input_asset
        self.__remove_protection_params: RemoveProtectionParams = remove_protection_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        remove_protection_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                remove_protection_request,
                                                OperationHeaderInfoEndpointMap.REMOVE_PROTECTION.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.REMOVE_PROTECTION_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        remove_protection_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            remove_protection_request = RemoveProtectionInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                             self.__remove_protection_params,
                                                                             notify_config_list)
        else:
            remove_protection_request = RemoveProtectionExternalAssetRequest(self.__input_asset,
                                                                             self.__remove_protection_params,
                                                                             notify_config_list,
                                                                             self.__output_asset)

        return remove_protection_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
