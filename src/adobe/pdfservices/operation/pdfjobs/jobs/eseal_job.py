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
from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.api.dto.request.esealpdf.eseal_pdf_external_asset_request import \
    ESealPDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.esealpdf.eseal_pdf_internal_asset_request import \
    ESealPDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params import PDFElectronicSealParams

class PDFElectronicSealJob(PDFServicesJob):
    """
    A job that allows clients to apply an electronic seal onto various PDF documents such as agreements, invoices, and more.

    To know more about PDF Electronic Seal, `Click Here <http://www.adobe.com/go/dc_eseal_overview_doc>`_.

    Sample usage.

    .. code-block:: python

        pdf_file = open('SOURCE_PATH', 'rb')
        file_input_stream = pdf_file.read()
        pdf_file.close()

        seal_image_file = open('IMAGE_SOURCE_PATH', 'rb')
        seal_image_input_stream = seal_image_file.read()
        seal_image_file.close()

        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )
        pdf_services = PDFServices(credentials=credentials)
        asset = pdf_services.upload(input_stream=file_input_stream, mime_type=PDFServicesMediaType.PDF)
        seal_image_asset = pdf_services.upload(input_stream=seal_image_input_stream, mime_type=PDFServicesMediaType.PNG)
        document_level_permission = DocumentLevelPermission.FORM_FILLING
        seal_field_name = "Signature1"
        seal_page_number = 1
        seal_visible = True
        field_location = FieldLocation(150, 250, 350, 200)
        field_options = FieldOptions(
            field_name=seal_field_name,
            field_location=field_location,
            page_number=seal_page_number,
            visible=seal_visible
        )
        provider_name = "<PROVIDER_NAME>"
        access_token = "<ACCESS_TOKEN>"
        credential_id = "<CREDENTIAL_ID>"
        pin = "<PIN>"
        csc_auth_context = CSCAuthContext(
            access_token=access_token,
            token_type="Bearer",
        )
        certificate_credentials = CSCCredentials(
            provider_name=provider_name,
            credential_id=credential_id,
            pin=pin,
            csc_auth_context=csc_auth_context,
        )
        electronic_seal_params = PDFElectronicSealParams(
            seal_certificate_credentials=certificate_credentials,
            seal_field_options=field_options,
        )
        electronic_seal_job = PDFElectronicSealJob(input_asset=asset,
                                                   electronic_seal_params=electronic_seal_params,
                                                   seal_image_asset=seal_image_asset)
        location = pdf_services.submit(electronic_seal_job)
        pdf_services_response = pdf_services.get_job_result(location, ESealPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

    """

    @enforce_types
    def __init__(self, input_asset: Asset, electronic_seal_params: PDFElectronicSealParams, *,
                 seal_image_asset: Optional[Asset] = None, output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`PDFElectronicSealJob` instance.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param electronic_seal_params: Parameters for electronic seal; can not be None.
        :type electronic_seal_params: PDFElectronicSealParams
        :param seal_image_asset: Seal image asset for the job. (Optional, use key-value)
        :type seal_image_asset: Asset
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of PDFElectronicSealJob.
        :rtype: PDFElectronicSealJob
        """
        self.__input_asset: Asset = input_asset
        self.__electronic_seal_params: PDFElectronicSealParams = electronic_seal_params
        self.__seal_image_asset: Asset = seal_image_asset
        self.__output_asset: Asset = output_asset
        ValidationUtil.validate_pdf_electronic_seal_params(electronic_seal_params)

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        eseal_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                eseal_pdf_request,
                                                OperationHeaderInfoEndpointMap.E_SEAL.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.ESEAL_PDF_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        eseal_pdf_request: PDFServicesAPIRequest
        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):
            seal_image_asset_id = self.__seal_image_asset.get_asset_id() if self.__seal_image_asset is not None else None
            eseal_pdf_request = ESealPDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                             seal_image_asset_id,
                                                             self.__electronic_seal_params, notify_config_list)
        else:
            eseal_pdf_request = ESealPDFExternalAssetRequest(self.__input_asset, self.__electronic_seal_params,
                                                             self.__seal_image_asset, notify_config_list,
                                                             self.__output_asset)

        return eseal_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__seal_image_asset is not None and not isinstance(self.__seal_image_asset,
                                                                  self.__input_asset.__class__):
            raise SdkException("Input asset and Seal Image Asset must be of same type")
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
