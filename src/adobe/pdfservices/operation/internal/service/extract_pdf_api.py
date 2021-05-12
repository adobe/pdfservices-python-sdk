# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
import mimetypes
from typing import List

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.api.cpf_api import CPFApi
from adobe.pdfservices.operation.internal.api.dto.request.extract_pdf_outputs import ExtractPDFOutputs
from adobe.pdfservices.operation.internal.api.dto.request.extract_pdf_params import ExtractPDFParams
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_content_analyzer_req import \
    CPFContentAnalyzerRequests
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_params import CPFParams
from adobe.pdfservices.operation.internal.api.dto.request.platform.inputs import Inputs
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.service.extract_data_parser import ExtractDataParser
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions


class ExtractPDFAPI:

    @staticmethod
    def extract_pdf(context: InternalExecutionContext, file_ref: FileRefImpl, extract_pdf_options: ExtractPDFOptions):
        extract_pdf_params = ExtractPDFParams.from_extract_pdf_options(extract_pdf_options)
        inputs = Inputs(mimetypes.types_map['.pdf'], CPFParams(extract_pdf_params))
        extract_service_id = context.client_config.get_cpf_extract_service_id()
        cpf_content_analyzer_req = CPFContentAnalyzerRequests(extract_service_id, inputs, ExtractPDFOutputs())
        logging.debug("Analyzer for the extract request %s ", cpf_content_analyzer_req.to_json())

        location = CPFApi.cpf_create_ops_api(context, cpf_content_analyzer_req, [file_ref],
                                             ServiceConstants.EXTRACT_OPERATION_NAME)
        return location

    @staticmethod
    def download_and_save(location, context, file_location):
        response = CPFApi.cpf_status_api(location, context)
        extract_data_parser = ExtractDataParser(response.content, response.headers[
            DefaultHeaders.CONTENT_TYPE_HEADER_NAME], file_location)
        try:
            extract_data_parser.parse()
        except Exception:
            CPFApi.logger.exception("Failed in parsing Extract Result")
            raise SdkException("Failed in parsing Extract Result : {content} ".format(
                content=response.content),
                request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, False))

