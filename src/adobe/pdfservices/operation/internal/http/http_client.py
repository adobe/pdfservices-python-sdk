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
import sys
from http import HTTPStatus
from typing import Callable, List

import pkg_resources
import requests

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil, CPF_STATUS, REPORT, ERROR_CODE, \
    STATUS, TITLE
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest

_logger = logging.getLogger(__name__)


def process_request(http_request: HttpRequest, success_status_codes: List,
                    error_response_handler: Callable[[requests.Response], None]):
    _append_default_headers(http_request.headers)
    if http_request.authenticator:
        # get token and append auth header
        access_token = http_request.authenticator.session_token().access_token
        http_request.headers[DefaultHeaders.AUTHORIZATION_HEADER_NAME] = "Bearer " + access_token
        http_request.headers[DefaultHeaders.X_API_KEY_HEADER_NAME] = http_request.authenticator.get_api_key()

    # retry the request if it fails with 401 and specific error code
    while (True):
        response = _execute_request(http_request)
        if _handle_response_and_retry(response, success_status_codes,
                                      error_response_handler, not http_request.authenticator) and http_request.retryable:
            _force_authenticate(http_request)
            # Only single retry is required in case of token expiry
            http_request.retryable = False
        else:
            return response


def _append_default_headers(headers: dict):
    # Set SDK Info header
    headers[DefaultHeaders.DC_APP_INFO_HEADER_KEY] = "{lang}-{name}-{version}".format(lang="python",
                                                                                      name='pdfservices-sdk',
                                                                                      version='1.0.1')
    headers[DefaultHeaders.ACCEPT_HEADER_NAME] = DefaultHeaders.JSON_TXT_CONTENT_TYPE


def _execute_request(http_request: HttpRequest):
    response = None
    timeout = (http_request.connect_timeout, http_request.read_timeout)
    try:
        if http_request.method == HttpMethod.POST:
            if http_request.data:
                response = requests.post(url=http_request.url,
                                         data=http_request.data,
                                         headers=http_request.headers,
                                         timeout=timeout)
            elif http_request.files:
                response = requests.post(url=http_request.url,
                                         files=http_request.files,
                                         headers=http_request.headers,
                                         timeout=timeout)
                for key, val in http_request.files.items():
                    if hasattr(val[1], 'close'):
                        val[1].close()
        elif http_request.method == HttpMethod.GET:
            response = requests.get(url=http_request.url, allow_redirects=True, headers=http_request.headers,
                                    timeout=timeout)
    except Exception:
        raise SdkException("Request could not be completed. Possible cause attached!", sys.exc_info())
    return response


def _force_authenticate(http_request: HttpRequest):
    _logger.debug("Re-authenticate as access_token is expired")
    access_token = http_request.authenticator.refresh_token().access_token
    http_request.headers[DefaultHeaders.AUTHORIZATION_HEADER_NAME] = "Bearer " + access_token


def _handle_response_and_retry(response: requests.Response, success_status_codes, error_response_handler, is_ims_api):
    if response.status_code not in success_status_codes:
        _logger.debug(
            "Failure response code {error_code} encountered from backend".format(error_code=response.status_code))
        should_retry = ResponseUtil.handle_api_failures(response, is_ims_api)
        return should_retry if should_retry else error_response_handler(response)
    elif response.status_code != HTTPStatus.ACCEPTED and "multipart" not in response.headers["Content-Type"]:
        content = json.loads(response.content)
        if content.get(CPF_STATUS, None):
            cpf_status = content.get(CPF_STATUS, None)
            report_error_code = "UNKNOWN"
            if cpf_status.get(REPORT, None):
                report_error_code = ResponseUtil._get_report_error_code(response_content=content)
            if cpf_status.get(STATUS, '') not in success_status_codes:
                raise OperationException(message="Error response received for request",
                                 request_tracking_id=ResponseUtil.get_request_tracking_id_from_response(response,
                                                                                                        False),
                                 status_code=cpf_status.get(STATUS, ''),
                                 error_message=cpf_status.get(TITLE, ""),
                                 report_error_code=report_error_code)


