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
from datetime import datetime
from http import HTTPStatus
from typing import List

import polling2
import requests

from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, SdkException
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_content_analyzer_req import \
    CPFContentAnalyzerRequests
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
from adobe.pdfservices.operation.internal.service.extract_data_parser import ExtractDataParser


class CPFApi:
    logger = logging.getLogger(__name__)

    @staticmethod
    def cpf_create_ops_api(context: InternalExecutionContext, analyzer_request: CPFContentAnalyzerRequests,
                           source_files: List[FileRefImpl], operation):

        start_time = datetime.now()
        multipart_dict: dict = {
            ServiceConstants.CONTENT_ANALYZER_REQUESTS_STRING:
                (
                    ServiceConstants.CONTENT_ANALYZER_REQUESTS_STRING,
                    analyzer_request.to_json(),
                    mimetypes.types_map['.json']
                )
        }
        for index, source_file_ref in enumerate(source_files):
            file_name = 'fileInput' + str(index + 1)
            multipart_dict[file_name] = (file_name, source_file_ref.get_as_stream())

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Upload req: url; %s", context.client_config.get_cpf_ops_create_uri())

        http_request = HttpRequest(http_method=HttpMethod.POST,
                                   url=context.client_config.get_cpf_ops_create_uri(),
                                   files=multipart_dict,
                                   headers={DefaultHeaders.X_DCSDK_OPS_INFO_HEADER_NAME: operation},
                                   authenticator=context.authenticator,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout())
        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.ACCEPTED],
                                               error_response_handler=CPFApi.handle_error_response)
        logging.debug("Upload Operation Latency(ms): %d", (datetime.now() - start_time).microseconds / 1000)
        return response.headers['location']

    @staticmethod
    def handle_error_response(response: requests.Response):
        pass

    @staticmethod
    def cpf_status_api(location, context: InternalExecutionContext):
        def is_correct_response(response):
            return response.status_code == HTTPStatus.OK

        start_time = datetime.now()
        http_request = HttpRequest(http_method=HttpMethod.GET,
                                   url=location,
                                   headers={},
                                   authenticator=context.authenticator,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout(),
                                   retryable=True)
        response = polling2.poll(
            lambda: http_client.process_request(http_request=http_request,
                                                success_status_codes=[HTTPStatus.OK, HTTPStatus.ACCEPTED],
                                                error_response_handler=CPFApi.handle_error_response),
            check_success=is_correct_response,
            step=0.5,
            timeout=10 * 60
        )
        logging.debug("Upload Operation Latency(ms): %d", (datetime.now() - start_time).microseconds / 1000)
        return response
