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
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.pdfjobs.params.pdf_watermark.pdf_watermark_params import PDFWatermarkParams
from adobe.pdfservices.operation.pdfjobs.params.pdf_watermark.watermark_appearance import WatermarkAppearance
from adobe.pdfservices.operation.internal.api.dto.request.pdfwatermark.pdf_watermark_params_payload import PDFWatermarkParamsPayload
from adobe.pdfservices.operation.internal.api.dto.request.pdfwatermark.pdf_watermark_input_payload import PDFWatermarkInputsPayload


class PDFWatermarkExternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'inputs': 'inputs',
        'output': 'output',
        'params': 'params',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset: Asset, watermark_asset: Asset, pdf_watermark_params: PDFWatermarkParams,
                 notify_config_list: List[NotifierConfig] = None,
                 output_asset: ExternalAsset = None):
        super().__init__()
        if input_asset is not None:
            self.inputs = PDFWatermarkInputsPayload(input_asset, watermark_asset)

        if output_asset is not None:
            self.output = output_asset

        self.params = PDFWatermarkParamsPayload(pdf_watermark_params)
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
