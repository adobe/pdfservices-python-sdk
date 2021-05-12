# Copyright 2021 Adobe. All rights reserved.
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

import requests

from adobe.pdfservices.operation.exception.exceptions import ServiceUsageException
from adobe.pdfservices.operation.internal.exceptions import OperationException

CPF_STATUS="cpf:status"
STATUS="status"
ERROR_CODE="error_code"
TITLE="title"
ERROR="error"
REASON="reason"
REPORT="report"
MESSAGE="message"

class ResponseUtil:
    _logger = logging.getLogger(__name__)
    CUSTOM_ERROR_MESSAGES_STATUS_CODE_MAPPING = {
        413: {
            ERROR_CODE: "RequestEntityTooLarge",
            MESSAGE: "Request entity too large"
        },
        502: {
            ERROR_CODE: "BadGateway",
            MESSAGE: "Bad gateway"
        },
        503: {
            ERROR_CODE: "ServiceUnavaibale",
            MESSAGE: "The Gateway servers are up, but overloaded with requests. Try again later."
        },
        504: {
            ERROR_CODE: "Gateway Timeout",
            MESSAGE: "The Gateway servers are up, but the request couldn't be serviced due to some failure within our stack. Try again later."
        },
    }
    # Service usage and quota exhaustion specific error code constants
    SERVICE_USAGE_EXCEPTION_STATUS_CODE_429001_STRING = "429001"
    SERVICE_USAGE_LIMIT_REACHED_ERROR_MESSAGE = "Service usage limit has been reached. " + \
                                                "Please retry after sometime."
    SERVICE_USAGE_EXCEPTION_STATUS_CODE_429002_STRING = "429002"
    INTEGRATION_SERVICE_USAGE_LIMIT_REACHED_ERROR_MESSAGE = "Service usage limit has been " + \
                                                            "reached for the integration. Please retry after sometime."
    QUOTA_ERROR_MESSAGE = "Either Quota for this operation is not available or Free trial quota is exhausted. Please visit " + \
                          "(www.adobe.com/go/pdftoolsapi_home) to start using free trial quota or (www.adobe.com/go/pdftoolsapi_err_quota) to upgrade to paid credentials."

    @staticmethod
    def handle_api_failures(response: requests.Response, is_ims_call=False):
        # Check if we need a custom error message for this status code
        custom_error_message = ResponseUtil.CUSTOM_ERROR_MESSAGES_STATUS_CODE_MAPPING.get(response.status_code)
        if custom_error_message:
            raise OperationException(message="Error response received for request",
                                     status_code=response.status_code,
                                     error_code=custom_error_message.get(ERROR_CODE),
                                     error_message=custom_error_message.get(MESSAGE),
                                     request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                            is_ims_call))
        # Special handling for service usage exception cases
        if response.status_code == 429:
            ResponseUtil.handle_service_usage_failure(response)
        # Handle CPF error response
        return ResponseUtil.handle_cpf_error_response(response)

    @staticmethod
    def get_request_tracking_id_from_response(response: requests.Response, is_ims_api_call):
        if is_ims_api_call:
            return response.headers.get("X-DEBUG-ID", None)
        else:
            return response.headers.get("x-request-id", None)

    @staticmethod
    def handle_service_usage_failure(response):
        response_content = json.loads(response.content)
        error_code = None
        if response_content.get(CPF_STATUS, None):
            if response_content.get(CPF_STATUS, {}).get(REPORT, None):
                error_code = ResponseUtil._get_report_error_code(response_content)
            response_content[MESSAGE] = ResponseUtil.QUOTA_ERROR_MESSAGE
        else:
            if ResponseUtil.SERVICE_USAGE_EXCEPTION_STATUS_CODE_429001_STRING == response_content.get(ERROR_CODE,
                                                                                                      None):
                response_content[MESSAGE] = ResponseUtil.SERVICE_USAGE_LIMIT_REACHED_ERROR_MESSAGE
            elif ResponseUtil.SERVICE_USAGE_EXCEPTION_STATUS_CODE_429002_STRING == response_content.get(ERROR_CODE,
                                                                                                        None):
                response_content[MESSAGE] = ResponseUtil.INTEGRATION_SERVICE_USAGE_LIMIT_REACHED_ERROR_MESSAGE
        raise ServiceUsageException(message=response_content.get(MESSAGE, None),
                                    request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                           False),
                                    error_code=error_code,
                                    status_code=response.status_code)

    @staticmethod
    def handle_cpf_error_response(response):
        response_content = json.loads(response.content)
        error_code = response_content.get(ERROR_CODE, None)
        error_message = response_content.get(MESSAGE, None)
        report_error_code = None
        if response_content.get(STATUS, None):
            error_code = response_content.get(STATUS, None)
            if response_content.get(TITLE, None):
                error_message = response_content.get(TITLE, None)
        elif response_content.get(REASON, None):
            error_code = response.status_code
            error_message = response_content.get(REASON, None)
        elif response_content.get(CPF_STATUS, None):
            if response_content.get(CPF_STATUS, {}).get(REPORT, None):
                report_error_code = ResponseUtil._get_report_error_code(response_content)
            error_code = response_content.get(CPF_STATUS, {}).get(STATUS, None)
            error_message = response_content.get(CPF_STATUS, {}).get(TITLE, None)
        elif response_content.get(ERROR, None):
            error_code = response.status_code
            error_message = response_content.get(ERROR, {}).get(MESSAGE, None)
        if response.status_code == 401 and error_code != "401013":
            return True
        raise OperationException(message="Error response received for request",
                                 request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                        False),
                                 error_code=error_code,
                                 status_code=response.status_code,
                                 error_message=error_message,
                                 report_error_code=report_error_code)

    @staticmethod
    def _get_report_error_code(response_content):
        stringify_report_json = response_content.get(CPF_STATUS, {}).get(REPORT, '{}')
        return json.loads(stringify_report_json).get(ERROR_CODE, None)
