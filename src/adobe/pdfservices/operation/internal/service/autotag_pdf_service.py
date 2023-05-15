# Copyright 2023 Adobe. All rights reserved.
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
from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.api.platform_api import PlatformApi
from adobe.pdfservices.operation.internal.constants.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.api.storage_api import StorageApi
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_request import AutotagPDFRequest


class AutotagPDFService:

    @staticmethod
    def autotag_pdf(context: InternalExecutionContext, source_file_ref: FileRef, autotag_pdf_options: AutotagPDFOptions,
                    x_request_id: str):

        try:
            get_upload_uri_response = StorageApi.get_upload_uri(context, source_file_ref.get_media_type(), x_request_id)

            content = json.loads(get_upload_uri_response.content)
            asset_id = content.get('assetID')
            StorageApi.upload_to_cloud(context, content.get('uploadUri'), source_file_ref)
            autotag_pdf_request = AutotagPDFRequest.from_autotag_pdf_options(asset_id, autotag_pdf_options)
            location = PlatformApi.submit_job(context, autotag_pdf_request, ServiceConstants.AUTOTAG_OPERATION_ENDPOINT,
                                              x_request_id, ServiceConstants.AUTOTAG_OPERATION_NAME)
            status_poll_response = PlatformApi.status_poll(context, location, x_request_id)

            download_uri_list = []
            taggedpdf_download_uri = json.loads(status_poll_response.content).get('tagged-pdf').get('downloadUri')
            download_uri_list.append(taggedpdf_download_uri)

            if autotag_pdf_options is not None and autotag_pdf_options.generate_report == True:
                report_download_uri = json.loads(status_poll_response.content).get('report').get('downloadUri')
                download_uri_list.append(report_download_uri)

            return download_uri_list
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            raise e
