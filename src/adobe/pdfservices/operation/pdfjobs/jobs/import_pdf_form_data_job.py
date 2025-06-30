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
from adobe.pdfservices.operation.internal.api.dto.request.importpdfformdata.import_pdf_form_data_external_asset_request import ImportPDFFormDataExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.importpdfformdata.import_pdf_form_data_internal_asset_request import ImportPDFFormDataInternalAssetRequest
from adobe.pdfservices.operation.internal.constants.operation_header_info_endpoint_map import OperationHeaderInfoEndpointMap
from adobe.pdfservices.operation.internal.constants.service_constants import custom_error_messages, ServiceConstants
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.pdf_services_helper import PDFServicesHelper
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.pdfjobs.params.import_pdf_form_data.import_pdf_form_data_params import ImportPDFFormDataParams
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob


class ImportPDFFormDataJob(PDFServicesJob):
    """
    A job that imports form data into a PDF using the provided JSON input.

    This sample demonstrates how to use Adobe PDF Services SDK to import form data
    into a PDF form. The process involves uploading a source PDF, providing form data
    in JSON format, and submitting an import form data job.

    Sample Usage:
        ```python
        import json
        from pathlib import Path

        from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
        from adobe.pdfservices.operation.pdf_services import PDFServices
        from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
        from adobe.pdfservices.operation.pdfjobs.jobs.import_pdf_form_data_job import ImportPDFFormDataJob
        from adobe.pdfservices.operation.pdfjobs.params.import_pdf_form_data.import_pdf_form_data_params import ImportPDFFormDataParams
        from adobe.pdfservices.operation.pdfjobs.result.import_pdf_form_data_result import ImportPDFFormDataResult

        # Initialize credentials
        credentials = ServicePrincipalCredentials(
            client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
            client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
        )

        # Create PDF services instance
        pdf_services = PDFServices(credentials=credentials)

        # Upload the input PDF
        with open('input_form.pdf', 'rb') as file:
            input_stream = file.read()
        
        input_asset = pdf_services.upload(
            input_stream=input_stream,
            mime_type=PDFServicesMediaType.PDF.mime_type
        )

        # Create form data to import
        form_data = {
            "option_two": "Yes",
            "option_one": "Yes", 
            "name": "sufia",
            "option_three": "Off",
            "age": "25",
            "favorite_movie": "Star Wars Again"
        }

        # Create import parameters
        import_params = ImportPDFFormDataParams(json_form_fields_data=form_data)

        # Create and configure the job
        import_job = ImportPDFFormDataJob(input_asset)
        import_job.set_params(import_params)

        # Submit the job
        location = pdf_services.submit(import_job)
        pdf_services_response = pdf_services.get_job_result(location, ImportPDFFormDataResult)

        # Get the result asset
        result_asset = pdf_services_response.get_result().get_asset()
        stream_asset = pdf_services.get_content(result_asset)

        # Save the result PDF
        with open('output_filled_form.pdf', 'wb') as output_file:
            output_file.write(stream_asset.get_input_stream())
        ```
    """

    @enforce_types
    def __init__(self, input_asset: Asset, *, output_asset: Optional[Asset] = None):
        """
        Constructs a new ImportPDFFormDataJob instance.

        :param input_asset: Asset object representing the input PDF with form fields; cannot be None.
        :type input_asset: Asset
        :param output_asset: Asset object representing the output asset. (Optional, use key-value)
        :type output_asset: Asset
        """
        self._input_asset = input_asset
        self._output_asset = output_asset
        self._import_pdf_form_data_params = None

    def set_params(self, import_pdf_form_data_params: ImportPDFFormDataParams):
        """
        Sets the Import PDF Form Data parameters.

        :param import_pdf_form_data_params: ImportPDFFormDataParams instance; cannot be None.
        :type import_pdf_form_data_params: ImportPDFFormDataParams
        :return: ImportPDFFormDataJob instance for method chaining
        :rtype: ImportPDFFormDataJob
        """
        if import_pdf_form_data_params is None:
            raise ValueError(custom_error_messages.get('GENERIC_CAN_NOT_BE_NULL', 'Parameter cannot be null').format('Import Form Data parameters'))
        
        self._import_pdf_form_data_params = import_pdf_form_data_params
        return self

    def set_output(self, output_asset: Asset):
        """
        Sets the output asset for the job.
        Note: External assets can be set as output only when input is external asset as well.

        :param output_asset: Asset object representing the output asset; cannot be None.
        :type output_asset: Asset
        :return: ImportPDFFormDataJob instance for method chaining
        :rtype: ImportPDFFormDataJob
        """
        if output_asset is None:
            raise ValueError(custom_error_messages.get('GENERIC_CAN_NOT_BE_NULL', 'Parameter cannot be null').format('Output asset'))
        
        if isinstance(self._input_asset, CloudAsset):
            raise ValueError(custom_error_messages.get('SET_OUTPUT_VALIDATE', 'Cannot set external output asset when input is cloud asset'))
        
        self._output_asset = output_asset
        return self

    def _process(self, execution_context: ExecutionContext, 
                 notify_config_list: Optional[List[NotifierConfig]] = None) -> str:
        """
        Process the import PDF form data job.

        :param execution_context: ExecutionContext for the job
        :type execution_context: ExecutionContext
        :param notify_config_list: List of notifier configurations (Optional)
        :type notify_config_list: List[NotifierConfig]
        :return: Job location URL
        :rtype: str
        """
        self._validate(execution_context)
        platform_api_request = self._generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid4())
        
        response = PDFServicesHelper.submit_job(
            execution_context,
            platform_api_request,
            OperationHeaderInfoEndpointMap.IMPORT_PDF_FORM_DATA.get_endpoint(),
            x_request_id,
            ServiceConstants.IMPORT_PDF_FORM_DATA_OPERATION_NAME
        )
        
        return response.headers.get('location')

    def _generate_platform_api_request(self, notify_config_list: Optional[List[NotifierConfig]]):
        """
        Generate the platform API request based on the asset type.

        :param notify_config_list: List of notifier configurations
        :type notify_config_list: List[NotifierConfig]
        :return: Platform API request object
        """
        if isinstance(self._input_asset, CloudAsset):
            return ImportPDFFormDataInternalAssetRequest(
                asset_id=self._input_asset.get_asset_id(),
                import_pdf_form_data_params=self._import_pdf_form_data_params,
                notifier_config_list=notify_config_list
            )
        else:
            external_request = ImportPDFFormDataExternalAssetRequest(
                input_asset=self._input_asset,
                import_pdf_form_data_params=self._import_pdf_form_data_params,
                notifier_config_list=notify_config_list
            )
            
            if self._output_asset:
                external_request.set_output(self._output_asset)
            
            return external_request

    def _validate(self, execution_context: ExecutionContext):
        """
        Validate the job configuration.

        :param execution_context: ExecutionContext for validation
        :type execution_context: ExecutionContext
        """
        if execution_context is None:
            raise ValueError("ExecutionContext cannot be None")
        
        if self._import_pdf_form_data_params is None:
            raise ValueError("Import PDF Form Data parameters must be set before processing") 