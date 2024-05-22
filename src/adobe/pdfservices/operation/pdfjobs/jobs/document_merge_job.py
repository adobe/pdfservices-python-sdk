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
from adobe.pdfservices.operation.internal.api.dto.request.document_generation.document_generation_external_asset_request import \
    DocumentMergeExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.document_generation.document_generation_internal_asset_request import \
    DocumentMergeInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.document_merge_params import DocumentMergeParams


class DocumentMergeJob(PDFServicesJob):
    """
    A job that enables the clients to produce high fidelity PDF and Word documents with dynamic data inputs.
    This operation merges the JSON data with the Word template to create dynamic documents for contracts and
    agreements, invoices, proposals, reports, forms, branded marketing documents and more.

    To know more about document generation and document templates,
    `Click Here <http://www.adobe.com/go/dcdocgen_overview_doc>`_.

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
                                          mime_type=MediaType.DOCX)
        json_data_for_merge = {"customerName": "Kane Miller", "customerVisits": 100}
        document_merge_params = DocumentMergeParams(json_data_for_merge=json_data_for_merge,
                                                    output_format=OutputFormat.DOCX)
        document_merge_job = DocumentMergeJob(input_asset=input_asset,
                                              document_merge_params=document_merge_params)
        location = pdf_services.submit(document_merge_job)
        pdf_services_response = pdf_services.get_job_result(location, DocumentMergePDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
    """

    @enforce_types
    def __init__(self, input_asset: Asset, document_merge_params: DocumentMergeParams, *,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`DocumentMergeJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param document_merge_params: DocumentMergeParams to set. can not be None.
        :type document_merge_params: DocumentMergeParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of DocumentMergeJob
        :rtype: DocumentMergeJob
        """
        self.__output_asset: Asset = output_asset
        self.__input_asset: Asset = input_asset
        self.__document_merge_params: DocumentMergeParams = document_merge_params
        ValidationUtil.validate_document_merge_params(document_merge_params)

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        document_merge_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                document_merge_request,
                                                OperationHeaderInfoEndpointMap.MERGE_DOCUMENT.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.DOCUMENT_MERGE_OPERATION_NAME)
        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        document_merge_request: PDFServicesAPIRequest

        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            document_merge_request = DocumentMergeInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                       self.__document_merge_params, notify_config_list)
        else:
            document_merge_request = DocumentMergeExternalAssetRequest(self.__input_asset,
                                                                       self.__document_merge_params,
                                                                       notify_config_list,
                                                                       self.__output_asset)

        return document_merge_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
