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

import logging
import sys
from typing import Callable, List

import requests

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http.response_util import ResponseUtil

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
    while True:
        response = _execute_request(http_request)
        if _handle_response_and_retry(response, success_status_codes,
                                      error_response_handler, not http_request.authenticator,
                                      http_request.request_key) and http_request.retryable:
            _force_authenticate(http_request)
            # Only single retry is required in case of token expiry
            http_request.retryable = False
        else:
            return response


def _append_default_headers(headers: dict):
    # Set SDK Info header
    headers[DefaultHeaders.DC_APP_INFO_HEADER_KEY] = "{lang}-{name}-{version}".format(lang="python",
                                                                                      name='pdfservices-sdk',
                                                                                      version='4.0.0')
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
                                         timeout=timeout,
                                         proxies=http_request.proxies.proxy_config_map() if
                                         http_request.proxies is not None else None)
            elif http_request.files:
                response = requests.post(url=http_request.url,
                                         files=http_request.files,
                                         headers=http_request.headers,
                                         timeout=timeout,
                                         proxies=http_request.proxies.proxy_config_map() if
                                         http_request.proxies is not None else None)
                for key, val in http_request.files.items():
                    if hasattr(val[1], 'close'):
                        val[1].close()
        elif http_request.method == HttpMethod.GET:
            response = requests.get(url=http_request.url, allow_redirects=True, headers=http_request.headers,
                                    timeout=timeout,
                                    proxies=http_request.proxies.proxy_config_map() if
                                    http_request.proxies is not None else None)
        elif http_request.method == HttpMethod.PUT:
            response = requests.put(url=http_request.url, data=http_request.data, headers=http_request.headers,
                                    timeout=timeout,
                                    proxies=http_request.proxies.proxy_config_map() if
                                    http_request.proxies is not None else None)
        elif http_request.method == HttpMethod.DELETE:
            response = requests.delete(url=http_request.url, headers=http_request.headers, timeout=timeout,
                                       proxies=http_request.proxies.proxy_config_map() if
                                       http_request.proxies is not None else None)

    except Exception as e:
        raise SdkException("Request could not be completed. Possible cause attached!", sys.exc_info())
    return response


def _force_authenticate(http_request: HttpRequest):
    _logger.debug("Re-authenticate as access_token is expired")
    access_token = http_request.authenticator.refresh_token().access_token
    http_request.headers[DefaultHeaders.AUTHORIZATION_HEADER_NAME] = "Bearer " + access_token


def _handle_response_and_retry(response: requests.Response, success_status_codes, error_response_handler, is_ims_api,
                               request_key: str):
    if response.status_code not in success_status_codes:
        _logger.debug(
            "Failure response code {error_code} encountered from backend".format(error_code=response.status_code))
        should_retry = ResponseUtil.handle_api_failures(response, request_key, is_ims_api)
        return should_retry if should_retry else error_response_handler(response)
