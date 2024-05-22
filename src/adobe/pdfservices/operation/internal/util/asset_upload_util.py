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

from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.stream_asset import StreamAsset


class AssetUploadUtil:

    def __init__(self, context: ExecutionContext, stream_asset: StreamAsset):
        self.__context = context
        self.__stream_asset = stream_asset

    def __call__(self):
        from adobe.pdfservices.operation.internal.pdf_services_helper import PDFServicesHelper
        return PDFServicesHelper.upload(self.__context, self.__stream_asset.get_input_stream(),
                                        self.__stream_asset.get_mime_type())
