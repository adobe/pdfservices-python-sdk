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

from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.api.platform_api import PlatformApi
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.api.dto.request.extract_pdf_request import ExtractPDFRequest
from adobe.pdfservices.operation.internal.api.storage_api import StorageApi


class ExtractPDFService:

    @staticmethod
    def extract_pdf(context: InternalExecutionContext, source_file_ref: FileRef, extract_pdf_options: ExtractPDFOptions,
                    x_request_id: str):

        try:
            get_upload_uri_response = StorageApi.get_upload_uri(context, source_file_ref.get_media_type(), x_request_id)

            content = json.loads(get_upload_uri_response.content)
            asset_id = content.get('assetID')
            StorageApi.upload_to_cloud(context, content.get('uploadUri'), source_file_ref)
            extract_pdf_request = ExtractPDFRequest.from_extract_pdf_options(asset_id, extract_pdf_options)
            location = PlatformApi.submit_job(context, extract_pdf_request, ServiceConstants.EXTRACT_OPERATION_ENDPOINT,
                                              x_request_id, ServiceConstants.EXTRACT_OPERATION_NAME)

            status_poll_response = PlatformApi.status_poll(context, location, x_request_id)
            download_uri = json.loads(status_poll_response.content).get('resource').get('downloadUri')
            return download_uri
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            raise e
