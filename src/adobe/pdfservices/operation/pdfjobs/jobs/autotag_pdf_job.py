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
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_external_asset_request import \
    AutotagPDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_internal_asset_request import \
    AutotagPDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.autotag_pdf.autotag_pdf_params import AutotagPDFParams


class AutotagPDFJob(PDFServicesJob):
    """
    A job that creates PDF documents with enhanced readability from existing PDF documents.
    An optional tagging report can also be generated which contains the information about the tags that the tagged
    output PDF document contains.

    Accessibility tags, used by assistive technology such as screen reader are required to make PDF files compliant.
    However, the generated PDF is not guaranteed to comply with accessibility standards such as WCAG and PDF/UA as
    there could be a need to perform further downstream remediation to meet those standards.

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
        autotag_pdf_job = AutotagPDFJob(input_asset)
        location = pdf_services.submit(autotag_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, AutotagPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_tagged_pdf()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, input_asset: Asset, *,
                 autotag_pdf_params: Optional[AutotagPDFParams] = None,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new instance of :samp:`AutotagPDFJob`.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param autotag_pdf_params: `AutotagPDFParams` to set.(Optional, use key-value)
        :type autotag_pdf_params: AutotagPDFParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of AutotagPDFJob
        :rtype: AutotagPDFJob
        """
        self.__input_asset: Asset = input_asset
        self.__autotag_pdf_params: AutotagPDFParams = autotag_pdf_params
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        autotag_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                autotag_pdf_request,
                                                OperationHeaderInfoEndpointMap.AUTO_TAG.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.AUTOTAG_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig]):
        autotag_pdf_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            autotag_pdf_request = AutotagPDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                 self.__autotag_pdf_params, notify_config_list)

        else:
            autotag_pdf_request = AutotagPDFExternalAssetRequest(self.__input_asset, self.__autotag_pdf_params,
                                                                 notify_config_list, self.__output_asset)

        return autotag_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
