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
from datetime import datetime
from http import HTTPStatus

import requests
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, SdkException
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.http.request_header_const import DefaultHeaders
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.api.dto.request.asset_upload_uri_request import AssetUploadURIRequest


class StorageApi:

    assets = "/assets"

    @staticmethod
    def upload_to_cloud(context: InternalExecutionContext, uri: str, source_file_ref: FileRef):
        try:
            http_request = HttpRequest(http_method=HttpMethod.PUT,
                                       request_key=RequestKey.UPLOAD,
                                       url=uri,
                                       data=source_file_ref.get_as_stream(),
                                       headers={DefaultHeaders.CONTENT_TYPE_HEADER_NAME: source_file_ref.get_media_type(
                                       )},
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout())
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
    def get_upload_uri(context: InternalExecutionContext, media_type: str, x_request_id: str):

        try:
            assetUploadURIRequest = AssetUploadURIRequest(media_type)

            http_request = HttpRequest(http_method=HttpMethod.POST,
                                       request_key=RequestKey.PLATFORM,
                                       url=context.client_config.get_pdf_services_uri() + StorageApi.assets,
                                       data=assetUploadURIRequest.to_json(),
                                       headers={DefaultHeaders.DC_REQUEST_ID_HEADER_KEY: x_request_id,
                                                DefaultHeaders.CONTENT_TYPE_HEADER_NAME: ExtensionMediaTypeMapping.JSON.mime_type}
                                       , authenticator=context.authenticator,
                                       connect_timeout=context.client_config.get_connect_timeout(),
                                       read_timeout=context.client_config.get_read_timeout())

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

    @staticmethod
    def download_and_save_file(context: InternalExecutionContext, uri: str,
                               destination_path: str):

        start_time = datetime.now()
        http_request = HttpRequest(http_method=HttpMethod.GET,
                                   request_key=RequestKey.DOWNLOAD,
                                   headers={},
                                   url=uri,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout())

        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.OK, HTTPStatus.ACCEPTED],
                                               error_response_handler=StorageApi.handle_error_response)
        logging.debug(f'Upload Operation Latency(ms): {(datetime.now() - start_time).microseconds / 1000}')

        logging.info(f'Downloading file to {destination_path}')

        file = FileRef.create_from_local_file(destination_path)
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        return file


