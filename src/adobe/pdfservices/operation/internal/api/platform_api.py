# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
import json
import logging
from datetime import datetime
from http import HTTPStatus
import polling2
from polling2 import TimeoutException
import requests

from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.internal.api.dto.response.job_status import JobStatus
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException
from adobe.pdfservices.operation.internal.api.dto.response.platform.platform_api_response import PlatformApiResponse
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.api.dto.request.platform.platform_api_request import PlatformApiRequest


class PlatformApi:
    operation = '/operation/'
    POLLING_TIMEOUT_STATUS_CODE = 0

    @staticmethod
    def submit_job(context: InternalExecutionContext, platform_api_request: PlatformApiRequest, operation_endpoint: str,
                   x_request_id: str, operation_header_info: str):
        http_request = HttpRequest(http_method=HttpMethod.POST,
                                   request_key=RequestKey.PLATFORM,
                                   url=context.client_config.get_pdf_services_uri() + PlatformApi.operation +
                                       operation_endpoint, data=platform_api_request.to_json(),
                                   headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id,
                                            DefaultHeaders.X_DCSDK_OPS_INFO_HEADER_NAME: operation_header_info,
                                            DefaultHeaders.CONTENT_TYPE_HEADER_NAME: ExtensionMediaTypeMapping.JSON.mime_type},

                                   authenticator=context.authenticator,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout())
        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.CREATED],
                                               error_response_handler=PlatformApi.handle_error_response)
        return response.headers.get('location')

    @staticmethod
    def status_poll(context: InternalExecutionContext, location: str, x_request_id: str):
        def is_correct_response(response):
            content = json.loads(response.content)
            status = content.get('status')
            if status == JobStatus.FAILED:
                job_error_response = PlatformApiResponse(status,content.get('error')).get_error_response()
                raise ServiceApiException(job_error_response.get('message'), ResponseUtil.
                                          get_request_tracking_id_from_response(response, False), job_error_response
                                          .get('status'), job_error_response.get('code'))
            return status == JobStatus.DONE

        start_time = datetime.now()
        http_request = HttpRequest(http_method=HttpMethod.GET,
                                   request_key=RequestKey.STATUS,
                                   url=location,
                                   headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id},
                                   authenticator=context.authenticator,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout(),
                                   retryable=True)

        try:
            response = polling2.poll(
                lambda: http_client.process_request(http_request=http_request,
                                                    success_status_codes=[HTTPStatus.OK, HTTPStatus.ACCEPTED],
                                                    error_response_handler=PlatformApi.handle_error_response),
                check_success=is_correct_response,
                step=0.5,
                timeout=10 * 60
            )
            logging.debug(f'Total polling time, Latency(ms): {(datetime.now() - start_time).microseconds / 1000}')
            return response
        except TimeoutException:
            logging.error("Polling Timeout reached. Something's wrong, file operation took too long")
            raise OperationException(message="Operation execution has timed out!", error_message="Polling Timeout reached", request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response, True)
                                     ,status_code=PlatformApi.POLLING_TIMEOUT_STATUS_CODE)


    @staticmethod
    def handle_error_response(response: requests.Response):
        pass
