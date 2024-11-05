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
from adobe.pdfservices.operation.internal.api.dto.request.pdfaccessibilitychecker.pdf_accessibility_checker_external_asset_request import \
    PDFAccessibilityCheckerExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.pdfaccessibilitychecker.pdf_accessibility_checker_internal_asset_request import \
    PDFAccessibilityCheckerInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.pdf_accessibility_checker.pdf_accessibility_checker_params import \
    PDFAccessibilityCheckerParams

class PDFAccessibilityCheckerJob(PDFServicesJob):
    """
    Accessibility Checker API will check PDF files to see if they meet the machine-verifiable requirements
    of PDF/UA and WCAG 2.0. It will generate a report that summarizes the findings of the accessibility checks.
    Additional human remediation may be required to ensure that the reading order of elements is correct and
    that alternative text tags properly convey the meaning of an image.

    The report contains links to documentation that assist in manually fixing problems using Adobe Acrobat Pro.

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
        pdf_accessibility_checker_job = PDFAccessibilityCheckerJob(input_asset)
        location = pdf_services.submit(pdf_accessibility_checker_job)
        pdf_services_response = pdf_services.get_job_result(location, PDFAccessibilityCheckerResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

        report_asset: CloudAsset = pdf_services_response.get_result().get_report()
        stream_report: StreamAsset = pdf_services.get_content(report_asset)
    """

    @enforce_types
    def __init__(self, input_asset: Asset, *, pdf_accessibility_checker_params: Optional[PDFAccessibilityCheckerParams] = None,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new instance of :samp:`PDFAccessibilityCheckerJob`.

        :param input_asset: The input asset for the job; can not be None.
        :type input_asset: Asset
        :param pdf_accessibility_checker_params: `PDFAccessibilityCheckerParams` to set.(Optional, use key-value)
        :type pdf_accessibility_checker_params: PDFAccessibilityCheckerParams
        :param output_asset: The output asset for the job. (Optional, use key-value)
        :type output_asset: ExternalAsset
        :return: A new instance of PDFAccessibilityCheckerJob
        :rtype: PDFAccessibilityCheckerJob
        """
        self.__input_asset = input_asset
        self.__pdf_accessibility_checker_params = pdf_accessibility_checker_params
        self.__output_asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)

        pdf_accessibility_checker_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context, pdf_accessibility_checker_request,
                                                OperationHeaderInfoEndpointMap.PDF_ACCESSIBILITY_CHECKER.get_endpoint(),
                                                x_request_id, ServiceConstants.PDF_ACCESSIBILITY_CHECKER_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        pdf_accessibility_checker_request: PDFServicesAPIRequest
        # check typecasting
        if isinstance(self.__input_asset, CloudAsset):

            input_asset = self.__input_asset.get_asset_id() if self.__input_asset is not None else None

            pdf_accessibility_checker_request = PDFAccessibilityCheckerInternalAssetRequest(input_asset,
                                                                                            self.__pdf_accessibility_checker_params,
                                                                                            notify_config_list)
        else:
            pdf_accessibility_checker_request = PDFAccessibilityCheckerExternalAssetRequest(self.__input_asset,
                                                                                            self.__pdf_accessibility_checker_params,
                                                                                            notify_config_list,
                                                                                            self.__output_asset)

        return pdf_accessibility_checker_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)

        if self.__input_asset is None:
            raise SdkException("Input asset cannot be None")

        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
