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
from http import HTTPStatus

import requests

from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, SdkException
from adobe.pdfservices.operation.internal.api.dto.request.asset_upload_uri_request import AssetUploadURIRequest
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType


class StorageApi:
    assets = "/assets"

    @staticmethod
    def upload_to_cloud(context: ExecutionContext, uri: str, input_stream, media_type):
        try:
            http_request = HttpRequest(http_method=HttpMethod.PUT,
                                       request_key=RequestKey.UPLOAD,
                                       url=uri,
                                       data=input_stream,
                                       headers={DefaultHeaders.CONTENT_TYPE_HEADER_NAME: media_type},
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       proxies=context.client_config.get_proxy_server_config())
            response = http_client.process_request(http_request=http_request,
                                                   success_status_codes=[HTTPStatus.ACCEPTED, HTTPStatus.OK],
                                                   error_response_handler=StorageApi.handle_error_response)

            logging.debug(f'Asset upload response {response}')

            return response
        except FileNotFoundError as fe:
            raise fe
        except IOError as io:
            raise SdkException(f'Unexpected error while uploading file {io}')

    @staticmethod
    def get_upload_uri(context: ExecutionContext, media_type: str, x_request_id: str):

        try:
            asset_upload_uri_request = AssetUploadURIRequest(media_type)

            http_request = HttpRequest(http_method=HttpMethod.POST,
                                       request_key=RequestKey.PLATFORM,
                                       url=context.client_config.get_pdf_services_uri() + StorageApi.assets,
                                       data=asset_upload_uri_request.to_json(),
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id,
                                                DefaultHeaders.CONTENT_TYPE_HEADER_NAME: PDFServicesMediaType.JSON.mime_type},
                                       authenticator=context.authenticator,
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       proxies=context.client_config.get_proxy_server_config())

            response = http_client.process_request(http_request=http_request,
                                                   success_status_codes=[HTTPStatus.ACCEPTED, HTTPStatus.OK],
                                                   error_response_handler=StorageApi.handle_error_response)
            return response

        except OperationException as oex:
            raise ServiceApiException(message=oex.error_message, error_code=oex.error_code,
                                      request_tracking_id=oex.request_tracking_id, status_code=oex.status_code)

    @staticmethod
    def get_download_uri(context: ExecutionContext, asset_id: str, x_request_id: str):

        try:
            http_request = HttpRequest(http_method=HttpMethod.GET,
                                       request_key=RequestKey.PLATFORM,
                                       url=context.client_config.get_pdf_services_uri() + StorageApi.assets + "/" + asset_id,
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id},
                                       authenticator=context.authenticator,
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout(),
                                       proxies=context.client_config.get_proxy_server_config())

            response = http_client.process_request(http_request=http_request,
                                                   success_status_codes=[HTTPStatus.ACCEPTED, HTTPStatus.OK],
                                                   error_response_handler=StorageApi.handle_error_response)
            return response

        except OperationException as oex:
            raise ServiceApiException(message=oex.error_message, error_code=oex.error_code,
                                      request_tracking_id=oex.request_tracking_id, status_code=oex.status_code)

    @staticmethod
    def handle_error_response(response: requests.Response):
        pass
