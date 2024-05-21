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
from adobe.pdfservices.operation.internal.api.dto.request.htmltopdf.html_to_pdf_external_asset_request import \
    HTMLtoPDFExternalAssetRequest
from adobe.pdfservices.operation.internal.api.dto.request.htmltopdf.html_to_pdf_internal_asset_request import \
    HTMLtoPDFInternalAssetRequest
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
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.html_to_pdf_params import HTMLtoPDFParams


class HTMLtoPDFJob(PDFServicesJob):
    """
    A job that converts a HTML file to a PDF file.

    An HTML input can be provided either as a local zip archive or as a static HTML file with inline CSS.
    Alternatively, an HTML can also be specified via URL.

    While creating the corresponding Asset instance, the media type must be:
        - "application/zip", if the input is a local zip archive.
        - "text/html", if the input is a static HTML file with inline CSS

    In case the input is a local zip archive, it must have the following structure:
        - The main HTML file must be named "index.html".
        - "index.html" must exist at the top level of zip archive, not in a folder.

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
        input_asset = pdf_services.upload(input_stream=input_stream, mime_type=MediaType.ZIP)
        page_layout = PageLayout(page_height=11.5, page_width=8)
        html_to_pdf_params =  HTMLtoPDFParams(page_layout=page_layout, include_header_footer=True)
        html_to_pdf_job = HTMLtoPDFJob(input_asset=input_asset, html_to_pdf_params=html_to_pdf_params)
        location = pdf_services.submit(html_to_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, HTMLtoPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)

    """

    @enforce_types
    def __init__(self, *, input_asset: Optional[Asset] = None,
                 input_url: Optional[str] = None,
                 html_to_pdf_params: Optional[HTMLtoPDFParams] = None,
                 output_asset: Optional[Asset] = None):
        """
        Constructs a new :samp:`HTMLtoPDFJob`.

        At least one of input_asset or input_url needs to be specified.

        :param input_asset: Asset object containing the input file. (Optional, use key-value)
        :type input_asset: Asset
        :param input_url: String representing the input URL. (Optional, use key-value)
        :type input_url: str
        :param html_to_pdf_params: HTMLToPDFParams}. (Optional, use key-value)
        :type html_to_pdf_params: HTMLtoPDFParams
        :param output_asset: Asset object representing the output asset. (Optional, use key-value)
        :type output_asset: Asset
        """

        if input_asset is None and input_url is None:
            raise SdkException("Either input_asset or input_url should be provided")
        if input_asset is not None and input_url is not None:
            raise SdkException("Both input_asset and input_url cannot be provided")

        self.__html_to_pdf_params: HTMLtoPDFParams = html_to_pdf_params
        self.__input_asset: Optional[Asset] = input_asset
        self.__input_url: Optional[str] = input_url
        self.__output_asset: Asset = output_asset

    def _process(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None) -> str:
        self._validate(execution_context, notify_config_list)
        html_to_pdf_pdf_request: PDFServicesAPIRequest = self.__generate_platform_api_request(notify_config_list)
        x_request_id = str(uuid.uuid1())

        response = PDFServicesHelper.submit_job(execution_context,
                                                html_to_pdf_pdf_request,
                                                OperationHeaderInfoEndpointMap.HTML_TO_PDF.get_endpoint(),
                                                x_request_id,
                                                ServiceConstants.HTML_TO_PDF_OPERATION_NAME)

        return response.headers.get('location')

    def __generate_platform_api_request(self, notify_config_list: List[NotifierConfig] = None):
        html_to_pdf_pdf_request: PDFServicesAPIRequest

        if self.__input_asset is not None:
            # check typecasting
            if isinstance(self.__input_asset, CloudAsset):
                html_to_pdf_pdf_request = HTMLtoPDFInternalAssetRequest(self.__input_asset.get_asset_id(),
                                                                        None,
                                                                        self.__html_to_pdf_params,
                                                                        notify_config_list)
            else:
                html_to_pdf_pdf_request = HTMLtoPDFExternalAssetRequest(self.__input_asset, self.__html_to_pdf_params,
                                                                        notify_config_list,
                                                                        self.__output_asset)

        else:
            html_to_pdf_pdf_request = HTMLtoPDFInternalAssetRequest(None,
                                                                    self.__input_url,
                                                                    self.__html_to_pdf_params,
                                                                    notify_config_list)

        return html_to_pdf_pdf_request

    def _validate(self, execution_context: ExecutionContext, notify_config_list: List[NotifierConfig] = None):
        super()._validate(execution_context)
        if self.__output_asset is not None and isinstance(self.__input_asset, CloudAsset):
            raise ValueError(CustomErrorMessages.SET_OUTPUT_VALIDATE)
