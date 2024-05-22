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

from typing import List, Any, Optional

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.config.client_config import ClientConfig
from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.pdf_services_helper import PDFServicesHelper
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.object_util import ObjectUtil
from adobe.pdfservices.operation.internal.util.string_util import StringUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services_job import PDFServicesJob
from adobe.pdfservices.operation.pdf_services_job_status_response import PDFServicesJobStatusResponse
from adobe.pdfservices.operation.pdf_services_response import PDFServicesResponse
from adobe.pdfservices.operation.pdfjobs.result.pdf_services_job_result import PDFServicesJobResult


class PDFServices:
    """
    This class is the entry point for all the PDF Service utilities.
    These utilities can be used to perform various functions such as submitting
    :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`,
    getting status of a :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`,
    getting result of a :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`,
    uploading :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`,
    getting content of an :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`,
    deleting an :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>` and refreshing an
    :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`.
    """

    @enforce_types
    def __init__(self, credentials: Credentials, *, client_config: Optional[ClientConfig] = None):
        """
        Constructs a new :samp:`PDFServices` instance with the given Credentials and ClientConfig.

        :param credentials: Credentials to be used for authentication; can not be None.
        :type credentials: Credentials
        :param client_config: Client configuration for PDFServices. (Optional, use key-value)
        :type client_config: ClientConfig
        """
        self.__executionContext: ExecutionContext = ExecutionContext(credentials, client_config)

    @enforce_types
    def submit(self, pdf_services_job: PDFServicesJob, *, notify_config_list: Optional[List] = None) -> str:
        """
        Creates the :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`
        and returns the polling URL.

        :param pdf_services_job: PDFServicesJob} to be submitted; can not be None.
        :type pdf_services_job: PDFServicesJob
        :param notify_config_list: List of
            :class:`NotifierConfig<adobe.pdfservices.operation.config.notifier.notifier_config.NotifierConfig>`
            to be used for notification. (Optional, use key-value)
        :type notify_config_list: list
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :raises ServiceUsageException: If service usage limits have been reached or credentials quota has been
            exhausted.
        :return: the polling URL.
        :rtype: str
        """
        return pdf_services_job._process(self.__executionContext, notify_config_list)

    @enforce_types
    def get_job_result(self, polling_url: str, result_type: PDFServicesJobResult.__class__) -> PDFServicesResponse:
        """
        Returns PDFServicesResponse for the submitted
        :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>` result.

        :param polling_url: URL to be polled to get the job result; can not be None.
        :type polling_url: str
        :param result_type: result class for
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`, it will be an
            implementation of PDFServicesJobResult; can not be None.
        :type result_type: PDFServicesJobResult.__class__
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :return: PDFServicesResponse for the submitted job.
        :rtype: PDFServicesResponse
        """

        if StringUtil.is_blank(polling_url):
            raise SdkException(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Polling URL"))
        ObjectUtil.require_not_null(result_type,
                                    CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Result class object"))

        return PDFServicesHelper.get_job_result(self.__executionContext, polling_url, result_type)

    @enforce_types
    def get_job_status(self, polling_url: str) -> PDFServicesJobStatusResponse:
        """
        :param polling_url: URL to be polled to get the job status; can not be None.
        :type polling_url: str
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :raises ServiceUsageException: If service usage limits have been reached or credentials quota has been
            exhausted.
        :return: Returns PDFServicesJobStatusResponse for the submitted
            :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
        :rtype: PDFServicesJobStatusResponse
        """
        if StringUtil.is_blank(polling_url):
            raise SdkException(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Polling URL"))
        return PDFServicesHelper.get_job_status(self.__executionContext, polling_url)

    @enforce_types
    def upload(self, input_stream: Any, mime_type: str) -> Asset:
        """
        Upload content from input stream and returns an :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`
        to be used in PDF Services SDK.

        Method will not close the input stream, responsibility of closing the input stream lies with the client.

        :param input_stream: input stream that is to be uploaded; can not be None.
        :param mime_type: mime type of the input stream; can not be None.
        :type mime_type: str
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :raises ServiceUsageException: If service usage limits have been reached or credentials quota has been
            exhausted.
        :return: asset containing the uploaded content
        :rtype: Asset
        """

        ObjectUtil.require_not_null(input_stream, CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Input stream"))
        if StringUtil.is_blank(mime_type):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Mime Type"))

        return PDFServicesHelper.upload(self.__executionContext, input_stream, mime_type)

    @enforce_types
    def upload_assets(self, upload_asset_list: List) -> []:
        """
        Upload content from list of :class:`StreamAsset<adobe.pdfservices.operation.io.stream_asset.StreamAsset>` and
        returns a list of :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>` to be used in PDF Services
        SDK.

        Method will not close the input stream of the Stream Asset, responsibility of closing the input stream lies
        with the client.

        :param upload_asset_list: :class:`StreamAsset<adobe.pdfservices.operation.io.stream_asset.StreamAsset>`
            list that is to be uploaded; can not be None.
        :type upload_asset_list: list
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :return: returns a list of :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>` to be used in PDF Services
            SDK.
        :rtype: list
        """

        ObjectUtil.require_not_null(upload_asset_list,
                                    CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Upload asset list"))
        if len(upload_asset_list) < 1:
            raise SdkException("Upload Asset List is empty.")
        for stream_asset in upload_asset_list:
            if stream_asset is None or not isinstance(stream_asset, StreamAsset):
                raise SdkException("Stream Asset List elements must be of the type StreamAsset.")

        return PDFServicesHelper.upload_assets(self.__executionContext, upload_asset_list)

    @enforce_types
    def get_content(self, asset: Asset) -> StreamAsset:
        """
        :param asset: Asset to the content; can not be None.
        :type asset: Asset
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :return: Returns the content of the asset.
        :rtype: StreamAsset
        """
        ObjectUtil.require_not_null(asset, CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Asset"))
        return PDFServicesHelper.get_content(self.__executionContext, asset)

    @enforce_types
    def refresh_download_uri(self, asset: Asset) -> Asset:
        """
        :param asset: asset to be refreshed; can not be None.
        :type asset: Asset
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        :return: a new Asset with a new valid download URI.
        :rtype: Asset
        """
        ObjectUtil.require_not_null(asset, CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Asset"))
        return PDFServicesHelper.refresh_download_uri(self.__executionContext, asset)

    @enforce_types
    def delete_asset(self, asset: Asset):
        """
        Deletes asset from PDF Services storage.

        :param asset: Asset to be deleted; can not be None.
        :type asset: Asset
        :raises ServiceApiException: If an error is encountered while submitting the job.
        :raises SdkException: Is thrown for client-side or network errors.
        """
        ObjectUtil.require_not_null(asset, CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE.format("Asset"))
        PDFServicesHelper.delete_asset(self.__executionContext, asset)
