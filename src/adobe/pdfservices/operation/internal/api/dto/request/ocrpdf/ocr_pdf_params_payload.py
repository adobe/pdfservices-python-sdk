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

from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.pdfjobs.params.ocr_pdf.ocr_params import OCRParams


class OCRParamsPayload:
    json_hint = {
        'ocr_lang': 'ocrLang',
        'ocr_type': 'ocrType'
    }

    def __init__(self, ocr_params: OCRParams):
        if ocr_params.get_ocr_type() is not None:
            self.ocr_lang = ocr_params.get_ocr_locale().get_locale()
        if ocr_params.get_ocr_locale() is not None:
            self.ocr_type = ocr_params.get_ocr_type().get_type()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
