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
from adobe.pdfservices.operation.pdfjobs.params.pdf_accessibility_checker.pdf_accessibility_checker_params import \
    PDFAccessibilityCheckerParams


class PDFAccessibilityCheckerParamsPayload:
    json_hint = {
        'page_start': 'pageStart',
        'page_end': 'pageEnd'
    }

    def __init__(self, pdf_accessibility_checker_params: PDFAccessibilityCheckerParams):
        self.page_start = pdf_accessibility_checker_params.get_page_start()
        self.page_end = pdf_accessibility_checker_params.get_page_end()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
