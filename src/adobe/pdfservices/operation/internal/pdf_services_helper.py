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

import concurrent
import json
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from http import HTTPStatus
from typing import List

from adobe.pdfservices.operation.exception.exceptions import SdkException, ServiceApiException, ServiceUsageException
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.api.dto.response.pdf_services_api.job_error_response import JobErrorResponse
from adobe.pdfservices.operation.internal.api.pdf_services_api import PDFServicesAPI
from adobe.pdfservices.operation.internal.api.storage_api import StorageApi
from adobe.pdfservices.operation.internal.constants.request_key import RequestKey
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.http import http_client
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod
from adobe.pdfservices.operation.internal.http.http_request import HttpRequest
from adobe.pdfservices.operation.internal.util.asset_upload_util import AssetUploadUtil
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services_job_status import PDFServicesJobStatus
from adobe.pdfservices.operation.pdf_services_job_status_response import PDFServicesJobStatusResponse
from adobe.pdfservices.operation.pdf_services_response import PDFServicesResponse
from adobe.pdfservices.operation.pdfjobs.result.autotag_pdf_result import AutotagPDFResult
from adobe.pdfservices.operation.pdfjobs.result.combine_pdf_result import CombinePDFResult
from adobe.pdfservices.operation.pdfjobs.result.compress_pdf_result import CompressPDFResult
from adobe.pdfservices.operation.pdfjobs.result.create_pdf_result import CreatePDFResult
from adobe.pdfservices.operation.pdfjobs.result.delete_pages_result import DeletePagesResult
from adobe.pdfservices.operation.pdfjobs.result.document_merge_result import DocumentMergePDFResult
from adobe.pdfservices.operation.pdfjobs.result.eseal_pdf_result import ESealPDFResult
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_result import ExportPDFResult
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_to_images_result import ExportPDFtoImagesResult
from adobe.pdfservices.operation.pdfjobs.result.extract_pdf_result import ExtractPDFResult
from adobe.pdfservices.operation.pdfjobs.result.html_to_pdf_result import HTMLtoPDFResult
from adobe.pdfservices.operation.pdfjobs.result.insert_pages_result import InsertPagesResult
from adobe.pdfservices.operation.pdfjobs.result.linearize_pdf_result import LinearizePDFResult
from adobe.pdfservices.operation.pdfjobs.result.ocr_pdf_result import OCRPDFResult
from adobe.pdfservices.operation.pdfjobs.result.pdf_properties_result import PDFPropertiesResult
from adobe.pdfservices.operation.pdfjobs.result.protect_pdf_result import ProtectPDFResult
from adobe.pdfservices.operation.pdfjobs.result.remove_protection_result import RemoveProtectionResult
from adobe.pdfservices.operation.pdfjobs.result.reorder_pages_result import ReorderPagesResult
from adobe.pdfservices.operation.pdfjobs.result.replace_page_result import ReplacePagesResult
from adobe.pdfservices.operation.pdfjobs.result.rotate_pages_result import RotatePagesResult
from adobe.pdfservices.operation.pdfjobs.result.split_pdf_result import SplitPDFResult


class PDFServicesHelper:
    _logger = logging.getLogger(__name__)

    @classmethod
    def upload(cls, context: ExecutionContext, input_stream, media_type: str) -> Asset:
        cls._logger.info("Started uploading asset")
        ValidationUtil.validate_execution_context(context)
        # Generating request id
        x_request_id = str(uuid.uuid1())
        cls._logger.debug(f"Uploading asset with request id {x_request_id}")

        get_upload_uri_response = StorageApi.get_upload_uri(context, media_type, x_request_id)
        content = json.loads(get_upload_uri_response.content)
        asset_id = content.get('assetID')
        StorageApi.upload_to_cloud(context, content.get('uploadUri'), input_stream, media_type)

        cls._logger.info("Finished uploading asset")
        return CloudAsset(asset_id)

    @classmethod
    def upload_assets(cls, context: ExecutionContext, stream_asset_list: []) -> []:
        cls._logger.info("Started uploading asset")
        ValidationUtil.validate_execution_context(context)

        assets = []

        # parallelize the uploads
        callable_tasks = [AssetUploadUtil(context, stream_asset_list[i]) for i in range(len(stream_asset_list))]
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(task) for task in callable_tasks]
        except Exception:
            raise SdkException("Error occurred while uploading assets.")

        for future in futures:
            try:
                assets.append(future.result(60 * 5))
            except concurrent.futures.TimeoutError:
                raise SdkException("Timeout occurred while waiting for future result.")
            except concurrent.futures.CancelledError:
                raise SdkException("Future was cancelled.")
            except Exception as ex:
                if isinstance(ex.__cause__, (ServiceApiException, SdkException, ServiceUsageException)):
                    raise ex.__cause__
                elif isinstance(ex.__cause__, OperationException):
                    oe = ex.__cause__
                    raise ServiceApiException(oe.error_message, oe.request_tracking_id, oe.status_code,
                                              oe.error_code)
                else:
                    raise SdkException("Error occurred while uploading.")
            finally:
                executor.shutdown(wait=False)

        executor.shutdown()
        # end of parallelize

        cls._logger.info("Finished uploading asset")
        return assets

    @classmethod
    def submit_job(cls, context: ExecutionContext, platform_api_request: PDFServicesAPIRequest, operation_endpoint: str,
                   x_request_id: str, operation_header_info: str):
        cls._logger.info(f"Started submitting {operation_header_info} job")
        cls._logger.debug(f"Submitting {operation_header_info} job with request id {x_request_id}")
        return PDFServicesAPI.submit_job(context, platform_api_request, operation_endpoint, x_request_id,
                                         operation_header_info)

    @classmethod
    def get_job_result(cls, context: ExecutionContext, location: str, result_type) -> PDFServicesResponse:
        cls._logger.info("Started getting job result")

        ValidationUtil.validate_execution_context(context)
        pdf_services_response = None
        while pdf_services_response is None or pdf_services_response.get_status() == PDFServicesJobStatus.IN_PROGRESS.get_value():
            pdf_services_response = cls.__poll_job(context, location, result_type)
            retry_after = pdf_services_response.get_retry_interval()

            try:
                cls._logger.debug(f"Retry polling for job result after {retry_after} seconds")
                time.sleep(retry_after)
            except KeyboardInterrupt:
                raise SdkException("Thread interrupted while waiting for operation execution status!!")

        cls._logger.info("Finished getting job result")
        return pdf_services_response

    @classmethod
    def __poll_job(cls, context: ExecutionContext, location: str, result_type) -> PDFServicesResponse:
        ValidationUtil.validate_execution_context(context)
        # generating x-request-id
        x_request_id = str(uuid.uuid4())
        cls._logger.debug(f"Started polling for status with request id {x_request_id}")

        try:
            pdf_services_response = PDFServicesAPI.status_poll(context, location, x_request_id)
            response_content_json = pdf_services_response.content
            response_headers = pdf_services_response.headers
            response_content = json.loads(response_content_json)
            response: PDFServicesResponse

            if response_content.get('status') == PDFServicesJobStatus.IN_PROGRESS.get_value():
                return PDFServicesResponse(status=response_content.get('status'),
                                           headers=response_headers,
                                           result=None)

            if response_content.get('status') == PDFServicesJobStatus.DONE.get_value():
                if result_type in cls.__get_single_asset_result_classes():
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(
                                                       CloudAsset(response_content.get('asset').get('assetID'),
                                                                  response_content.get('asset').get('downloadUri')))
                                                   )

                elif result_type == AutotagPDFResult:
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(
                                                       CloudAsset(response_content.get('tagged-pdf').get('assetID'),
                                                                  response_content.get('tagged-pdf').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'tagged-pdf') else None,
                                                       CloudAsset(response_content.get('report').get('assetID'),
                                                                  response_content.get('report').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'report') else None,
                                                       CloudAsset(response_content.get('resource').get('assetID'),
                                                                  response_content.get('resource').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'resource') else None,
                                                   )
                                                   )

                elif result_type == ExtractPDFResult:
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(
                                                       CloudAsset(response_content.get('content').get('assetID'),
                                                                  response_content.get('content').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'content') else None,
                                                       CloudAsset(response_content.get('resource').get('assetID'),
                                                                  response_content.get('resource').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'resource') else None,
                                                       PDFServicesHelper.__fetch_extract_content_json(
                                                           context,
                                                           response_content.get('content').get('downloadUri')).
                                                       content if response_content.get('content') else None
                                                   ))

                elif result_type == ExportPDFtoImagesResult:
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(
                                                       [CloudAsset(asset.get('assetID'), asset.get('downloadUri')) for
                                                        asset
                                                        in
                                                        response_content.get('assetList')]
                                                       if response_content.get('assetList') else None
                                                   ))

                elif result_type == SplitPDFResult:
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(
                                                       [CloudAsset(asset.get('assetID'), asset.get('downloadUri')) for
                                                        asset
                                                        in
                                                        response_content.get('assetList')]
                                                       if response_content.get('assetList') else None,
                                                       CloudAsset(response_content.get('asset').get('assetID'),
                                                                  response_content.get('asset').get(
                                                                      'downloadUri')) if response_content.get(
                                                           'asset') else None
                                                   ))

                elif result_type == PDFPropertiesResult:
                    response = PDFServicesResponse(status=response_content.get('status'),
                                                   headers=response_headers,
                                                   result=result_type(response_content.get('metadata')))

                else:
                    raise SdkException(message="No result class found.")

        except (AttributeError, TypeError) as ex:
            raise SdkException("Error occurred while polling")
        except OperationException as oe:
            raise ServiceApiException(oe.message, oe.request_tracking_id, oe.status_code, oe.error_code)

        if response_content.get('status') == PDFServicesJobStatus.FAILED.get_value():
            error_response = JobErrorResponse(response_content)
            raise ServiceApiException(message=error_response.get_message(),
                                      request_tracking_id=response_headers.get('x-request-id', None),
                                      status_code=error_response.get_status(),
                                      error_code=error_response.get_code())

        cls._logger.info("Finished polling for status")
        return response

    @classmethod
    def get_job_status(cls, context: ExecutionContext, location: str):
        cls._logger.info("Started getting job status")

        ValidationUtil.validate_execution_context(context)

        x_request_id = str(uuid.uuid4())
        pdf_services_response = PDFServicesAPI.status_poll(context, location, x_request_id)

        response_content_json = pdf_services_response.content
        response_headers = pdf_services_response.headers
        response_content = json.loads(response_content_json)

        cls._logger.info("Finished getting job status")
        return PDFServicesJobStatusResponse(status=response_content.get('status'),
                                            headers=response_headers)

    # ADD TRY-EXCEPT BLOCK TO THIS AND ALL OTHER METHODS
    @classmethod
    def get_content(cls, context: ExecutionContext, asset: Asset) -> StreamAsset:
        cls._logger.info("Started getting content")
        ValidationUtil.validate_execution_context(context)
        asset.__class__ = CloudAsset
        uri = asset.get_download_uri()

        cls._logger.debug(f"Getting content for asset id {asset.get_asset_id()}")
        start_time = datetime.now()
        http_request = HttpRequest(http_method=HttpMethod.GET,
                                   request_key=RequestKey.DOWNLOAD,
                                   headers={},
                                   url=uri,
                                   connect_timeout=context.client_config.get_connect_timeout(),
                                   read_timeout=context.client_config.get_read_timeout(),
                                   proxies=context.client_config.get_proxy_server_config())

        response = http_client.process_request(http_request=http_request,
                                               success_status_codes=[HTTPStatus.OK, HTTPStatus.ACCEPTED],
                                               error_response_handler=StorageApi.handle_error_response)
        logging.debug(f'Upload Operation Latency(ms): {(datetime.now() - start_time).microseconds / 1000}')

        cls._logger.info("Finished getting content")
        return StreamAsset(response.content, response.headers.get('content-type'))

    @classmethod
    def refresh_download_uri(cls, context: ExecutionContext, asset: Asset) -> CloudAsset:
        cls._logger.info("Started refreshing asset")
        ValidationUtil.validate_execution_context(context)

        if not isinstance(asset, CloudAsset):
            raise SdkException("Only internal storage is supported for refreshing download URI.")

        # generating x-request-id
        x_request_id = str(uuid.uuid1())
        asset_id = asset.get_asset_id()

        cls._logger.debug(f"Refreshing asset with asset id {asset_id} and request id {x_request_id}")
        try:
            get_download_uri_response = StorageApi.get_download_uri(context, asset_id, x_request_id)

        except OperationException as e:
            raise ServiceApiException(message=e.error_message, error_code=e.error_code,
                                      request_tracking_id=e.request_tracking_id, status_code=e.status_code)

        except Exception as e:
            raise SdkException("Unexpected error occurred while refreshing download URI.")

        cls._logger.info("Finished refreshing asset")
        return CloudAsset(asset_id, json.loads(get_download_uri_response.content).get('downloadUri'))

    @classmethod
    def delete_asset(cls, context: ExecutionContext, asset: Asset):
        cls._logger.info("Started deleting asset")

        ValidationUtil.validate_execution_context(context)
        if not isinstance(asset, CloudAsset):
            raise SdkException("Only internal storage is supported for delete asset.")

        # generating x-request-id
        x_request_id = str(uuid.uuid4())
        asset_id = asset.get_asset_id()

        cls._logger.debug(f"Deleting asset with asset id {asset_id} and request id {x_request_id}")

        PDFServicesAPI.delete_asset(context, asset_id, x_request_id)

        cls._logger.info("Finished deleting asset")

    @classmethod
    def __get_single_asset_result_classes(cls) -> List:
        return [LinearizePDFResult, DocumentMergePDFResult, DeletePagesResult,
                RotatePagesResult, ESealPDFResult, CompressPDFResult,
                CombinePDFResult, ExportPDFResult, OCRPDFResult, ProtectPDFResult,
                InsertPagesResult, ReplacePagesResult, ReorderPagesResult,
                CreatePDFResult, HTMLtoPDFResult, RemoveProtectionResult]

    @classmethod
    def __fetch_extract_content_json(cls, context: ExecutionContext, download_uri: str):
        x_request_id = str(uuid.uuid1())
        return PDFServicesAPI.get_response(context, download_uri, x_request_id)
