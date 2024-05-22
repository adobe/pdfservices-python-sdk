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

import json
import logging
from xml.etree.ElementTree import fromstring
from xml.sax import SAXParseException

import requests

from adobe.pdfservices.operation.exception.exceptions import ServiceUsageException, ServiceApiException
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.exceptions import OperationException

STATUS = "status"
ERROR_CODE = "error_code"
ERROR = "error"
MESSAGE = "message"
CODE = "code"


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
    def handle_api_failures(response: requests.Response, request_key, is_ims_call=False):
        # Check if we need a custom error message for this status code
        custom_error_message = ResponseUtil.CUSTOM_ERROR_MESSAGES_STATUS_CODE_MAPPING.get(response.status_code)
        if custom_error_message:
            raise OperationException(message="Error response received for request",
                                     status_code=response.status_code,
                                     error_code=custom_error_message.get(ERROR_CODE),
                                     error_message=custom_error_message.get(MESSAGE),
                                     request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                            is_ims_call))
        ResponseUtil.handle_upload_asset_failure(response, request_key)
        # Special handling for service usage exception cases
        if response.status_code == 429:
            ResponseUtil.handle_service_usage_failure(response)
        # Handle CPF error response
        return ResponseUtil.handle_service_api_error_response(response)

    @staticmethod
    def get_request_tracking_id_from_response(response: requests.Response, is_ims_api_call):
        if is_ims_api_call:
            return response.headers.get("X-DEBUG-ID", None)
        else:
            return response.headers.get("x-request-id", None)

    @staticmethod
    def handle_service_usage_failure(response: requests.Response):
        response_content = json.loads(response.content)
        error_code = response_content.get('error').get('code')
        message = response_content.get('error').get('message')
        raise ServiceUsageException(message=message,
                                    request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                           False),
                                    error_code=error_code,
                                    status_code=response.status_code)

    @staticmethod
    def handle_upload_asset_failure(response: requests.Response, request_key: str):
        if request_key == RequestKey.UPLOAD:
            try:
                response_content = fromstring(response.content)
                error_code = response_content.find('Code').text
                request_id = response_content.find('RequestId').text
                error_message = response_content.find('Message').text
                status_code = response.status_code
            except SAXParseException:
                raise ServiceApiException("Error in uploading file")
            raise OperationException(message="Error response received for request", status_code=status_code,
                                     request_tracking_id=request_id, error_message=error_message, error_code=error_code)

    @staticmethod
    def handle_service_api_error_response(response):
        response_content = json.loads(response.content)
        error_content = response_content.get(ERROR, None)
        # For 429 cases
        error_code = response_content.get(ERROR_CODE, None)
        message = response_content.get(MESSAGE, None)
        # For all other cases
        if error_content is not None:
            error_code = error_content.get(CODE, None)
            message = error_content.get(MESSAGE, None)

        raise ServiceApiException(message=message,
                                  request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                         False),
                                  status_code=response.status_code,
                                  error_code=error_code)
