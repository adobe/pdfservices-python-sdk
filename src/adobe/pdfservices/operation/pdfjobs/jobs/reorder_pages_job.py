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
from adobe.pdfservices.operation.pdfjobs.params.reorder_pages.reorder_pages_params import ReorderPagesParams


class ReorderPagesJob(PDFServicesJob):
    """
    A job that allows to rearrange pages in a PDF file according to the specified order.

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
        pages_to_reorder = PageRanges().add_range(3, 4)
                            .add_single_page(1)
        reorder_pages_params = ReorderPagesParams(asset=input_asset, page_ranges=pages_to_reorder)
        reorder_pages_job = ReorderPagesJob(reorder_pages_params=reorder_pages_params)
        location = pdf_services.submit(reorder_pages_job)
        pdf_services_response = pdf_services.get_job_result(location, ReorderPagesResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, reorder_pages_params: ReorderPagesParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`ReorderPagesJob` instance.

        :param reorder_pages_params: `ReorderPagesParams` to set; can not be None.
        :type reorder_pages_params: ReorderPagesParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of `ReorderPagesJob`.
        :rtype: ReorderPagesJob
        """
        self.__reorder_pages_params: ReorderPagesParams = reorder_pages_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        reorder_pages_request = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                reorder_pages_request,
                                                OperationHeaderInfoEndpointMap.REORDER_PAGES.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.REORDER_PAGES_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None) -> PDFServicesAPIRequest:
        combine_pdf_params = CombinePDFParams()
        combine_pdf_params.add_asset(self.__reorder_pages_params.get_asset(),
                                     page_ranges=self.__reorder_pages_params.get_page_ranges())

        reorder_pages_request: PDFServicesAPIRequest

        if isinstance(self.__reorder_pages_params.get_asset(), CloudAsset):
            reorder_pages_request = CombinePDFInternalAssetRequest(combine_pdf_params,
                                                                   notify_config_list)
        else:
            reorder_pages_request = CombinePDFExternalAssetRequest(combine_pdf_params,
                                                                   notify_config_list,
                                                                   self.__output_asset)
        return reorder_pages_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__reorder_pages_params.get_asset(), CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
