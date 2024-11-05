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
from adobe.pdfservices.operation.pdfjobs.params.pdf_watermark.pdf_watermark_params import PDFWatermarkParams


class PDFWatermarkParamsPayload:
    json_hint = {
        'page_ranges': 'pageRanges',
        'appearance': 'appearance'
    }

    def __init__(self, pdf_watermark_params: PDFWatermarkParams):
        if pdf_watermark_params is None:
            return
        if pdf_watermark_params.get_page_ranges() is not None:
            self.page_ranges = pdf_watermark_params.get_page_ranges().ranges
        if pdf_watermark_params.get_watermark_appearance() is not None:
            self.appearance = pdf_watermark_params.get_watermark_appearance()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
