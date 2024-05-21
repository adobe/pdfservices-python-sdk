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
from adobe.pdfservices.operation.pdfjobs.params.autotag_pdf.autotag_pdf_params import AutotagPDFParams


class AutotagPDFParamsPayload:
    json_hint = {
        'shift_headings': 'shiftHeadings',
        'generate_report': 'generateReport'
    }

    def __init__(self, autotag_pdf_params: AutotagPDFParams):
        self.shift_headings = autotag_pdf_params.get_shift_headings()
        self.generate_report = autotag_pdf_params.get_generate_report()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
