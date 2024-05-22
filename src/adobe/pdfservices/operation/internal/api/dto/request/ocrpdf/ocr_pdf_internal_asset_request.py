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
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_params import OCRParams


class OCRPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'ocr_lang': 'ocrLang',
        'ocr_type': 'ocrType',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset_id: str, ocr_pdf_params: OCRParams, notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = input_asset_id
        if ocr_pdf_params is not None:
            self.ocr_lang = ocr_pdf_params.get_ocr_locale().get_locale()
            self.ocr_type = ocr_pdf_params.get_ocr_type().get_type()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
