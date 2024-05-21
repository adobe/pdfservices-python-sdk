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
from adobe.pdfservices.operation.internal.api.dto.request.pdf_properties.pdf_properties_external_asset_request import \
    PDFPropertiesExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pdf_properties.pdf_properties_internal_asset_request import \
    PDFPropertiesInternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.constants.operation_header_info_endpoint_map import \
    OperationHeaderInfoEndpointMap
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.pdf_services_helper import PDFServicesHelper
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob
from adobe.pdfservices.operation.pdfjobs.params.pdf_properties.pdf_properties_params import PDFPropertiesParams


class PDFPropertiesJob(PDFServicesJob):
    """
    A job that is used to fetch properties from an input PDF file. The properties are returned in a dict.

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
        input_asset = pdf_services.upload(input_stream=input_stream,
                                          mime_type=MediaType.PDF)
        pdf_properties_params = PDFPropertiesParams(include_page_level_properties=True)
        pdf_properties_job = PDFPropertiesJob(input_asset=input_asset, pdf_properties_params=pdf_properties_params)
        location = pdf_services.submit(pdf_properties_job)
        pdf_services_response = pdf_services.get_job_result(location, PDFPropertiesResult)
        pdf_properties_result = pdf_services_response.get_result()

    """

    @enforce_types
    def __init__(self, input_asset: Asset, *,
                 pdf_properties_params: Optional[PDFPropertiesParams] = None):
        """
        Constructs a new :samp:`PDFPropertiesJob` instance.

        :param input_asset: Asset object containing the input file; can not be None.
        :type input_asset: Asset
        :param pdf_properties_params: PDFPropertiesParams object containing the properties to be fetched.
            (Optional, use key-value)
        :type pdf_properties_params: PDFPropertiesParams
        :param output_asset: Asset object representing the output asset. (Optional, use key-value)
        :type output_asset: ExternalAsset
        """
        self.__input_asset: Asset = input_asset
        self.__pdf_properties_params: PDFPropertiesParams = pdf_properties_params

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        pdf_properties_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                pdf_properties_request,
                                                OperationHeaderInfoEndpointMap.PDF_PROPERTIES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.PDF_PROPERTIES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        pdf_properties_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            pdf_properties_request = PDFPropertiesInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                       self.__pdf_properties_params, notify_config_list)
        else:
            pdf_properties_request = PDFPropertiesExternalAssetRequest(self.__input_asset, self.__pdf_properties_params,
                                                                       notify_config_list)

        return pdf_properties_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
