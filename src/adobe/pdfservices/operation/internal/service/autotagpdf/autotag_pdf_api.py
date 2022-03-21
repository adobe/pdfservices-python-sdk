# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.api.cpf_api import CPFApi
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_output_without_report import \
    AutotagPDFOutputWithoutReport
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_params import AutotagPDFParams
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_output_with_report import AutotagPDFOutputWithReport
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_content_analyzer_req import CPFContentAnalyzerRequests
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_params import CPFParams
from adobe.pdfservices.operation.internal.api.dto.request.platform.inputs import Inputs
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.service.autotagpdf.autotag_data_parser import AutotagDataParser
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions


class AutotagPDFAPI:

    @staticmethod
    def autotag_pdf(context: InternalExecutionContext, file_ref: FileRefImpl, autotag_pdf_options: AutotagPDFOptions):
        autotag_pdf_params = AutotagPDFParams.from_autotag_pdf_options(autotag_pdf_options)
        inputs = Inputs(ExtensionMediaTypeMapping.PDF, CPFParams(autotag_pdf_params))
        autotag_service_id = context.client_config.get_cpf_autotag_service_id()
        if autotag_pdf_options.generate_report == True:
            autotag_pdf_output = AutotagPDFOutputWithReport()
        else:
            autotag_pdf_output = AutotagPDFOutputWithoutReport()
        cpf_content_analyzer_req = CPFContentAnalyzerRequests(autotag_service_id, inputs, autotag_pdf_output)
        logging.debug("Analyzer for the autotag request %s ", cpf_content_analyzer_req.to_json())

        location = CPFApi.cpf_create_ops_api(context, cpf_content_analyzer_req, [file_ref],
                                             ServiceConstants.AUTOTAG_OPERATION_NAME)
        return location

    @staticmethod
    def download_and_save(location, context, file_location_pdf, file_location_xlsx):
        response = CPFApi.cpf_status_api(location, context)
        autotag_data_parser = AutotagDataParser(response.content, response.headers[
            DefaultHeaders.CONTENT_TYPE_HEADER_NAME], file_location_pdf, file_location_xlsx)
        try:
            return autotag_data_parser.parse()
        except Exception:
            raise SdkException("Failed in parsing Autotag Result : {content} ".format(
                content=response.content),
                request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, False))
