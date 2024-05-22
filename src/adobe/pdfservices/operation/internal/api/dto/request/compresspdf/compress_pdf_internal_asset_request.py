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

import json
from typing import List

from adobe.pdfservices.operation.config.notifier.notifier_config import NotifierConfig
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compress_pdf_params import CompressPDFParams
from adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compression_level import CompressionLevel


class CompressPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'compression_level': 'compressionLevel',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset_id: str, compress_pdf_params: CompressPDFParams,
                 notify_config_list: List[NotifierConfig]):
        super().__init__()
        self.asset_id = input_asset_id
        self.compression_level = CompressionLevel.MEDIUM.get_compression_level()
        if compress_pdf_params is not None:
            self.compression_level = compress_pdf_params.get_compression_level().get_compression_level()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
