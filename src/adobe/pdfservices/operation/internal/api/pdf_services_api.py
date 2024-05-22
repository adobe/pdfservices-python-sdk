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

from http import HTTPStatus

import requests

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType


class PDFServicesAPI:
    operation = '/operation/'
    assets = '/assets/'
    POLLING_TIMEOUT_STATUS_CODE = 0

    @staticmethod
    def submit_job(context: ExecutionContext, platform_api_request: PDFServicesAPIRequest, operation_endpoint: str,
                   x_request_id: str, operation_header_info: str):
        try:
            http_request = HttpRequest(http_method=HttpMethod.POST,
                                       request_key=RequestKey.PLATFORM,
                                       url=context.client_config.get_pdf_services_uri() + PDFServicesAPI.operation +
                                           operation_endpoint,
                                       data=platform_api_request.to_json(),
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id,
                                                DefaultHeaders.X_DCSDK_OPS_INFO_HEADER_NAME: operation_header_info,
                                                DefaultHeaders.CONTENT_TYPE_HEADER_NAME: PDFServicesMediaType.JSON.mime_type},

                                       authenticator=context.authenticator,
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       proxies=context.client_config.get_proxy_server_config())
        except Exception as ex:
            raise SdkException("Error generating http request for submitting the job.")
        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.CREATED],
                                               error_response_handler=PDFServicesAPI.handle_error_response)
        return response

    @staticmethod
    def status_poll(context: ExecutionContext, location: str, x_request_id: str):
        ValidationUtil.validate_execution_context(context)

        http_request = HttpRequest(http_method=HttpMethod.GET,
                                   request_key=RequestKey.STATUS,
                                   url=location,
                                   headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id},
                                   authenticator=context.authenticator,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout(),
                                   retryable=True,
                                   proxies=context.client_config.get_proxy_server_config())

        return http_client.process_request(http_request=http_request,
                                           success_status_codes=[HTTPStatus.OK, HTTPStatus.ACCEPTED],
                                           error_response_handler=PDFServicesAPI.handle_error_response)

    @staticmethod
    def handle_error_response(response: requests.Response):
        pass

    @staticmethod
    def get_response(context: ExecutionContext, location: str, x_request_id: str):
        try:
            http_request = HttpRequest(http_method=HttpMethod.GET,
                                       request_key=RequestKey.PLATFORM,
                                       url=location,
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id},
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       retryable=True,
                                       proxies=context.client_config.get_proxy_server_config())
        except Exception as ex:
            raise SdkException("Error generating http request for submitting the job.")
        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.OK],
                                               error_response_handler=PDFServicesAPI.handle_error_response)
        return response

    @staticmethod
    def delete_asset(context: ExecutionContext, asset_id: str, x_request_id: str):
        try:
            http_request = HttpRequest(http_method=HttpMethod.DELETE,
                                       request_key=RequestKey.PLATFORM,
                                       url=context.client_config.get_pdf_services_uri() + PDFServicesAPI.assets +
                                           asset_id,
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id},
                                       authenticator=context.authenticator,
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       retryable=True,
                                       proxies=context.client_config.get_proxy_server_config())
        except Exception as ex:
            raise SdkException("Error generating http request for submitting the job.")
        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.NO_CONTENT],
                                               error_response_handler=PDFServicesAPI.handle_error_response)

        return response
