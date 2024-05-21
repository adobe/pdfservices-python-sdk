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
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams


class ExportPDFParamsPayload:
    json_hint = {
        'target_format': 'targetFormat',
        'ocr_lang': 'ocrLang'
    }

    def __init__(self, export_pdf_params: ExportPDFParams):
        self.target_format = export_pdf_params.get_target_format().get_file_ext()
        self.ocr_lang = export_pdf_params.get_ocr_lang().get_export_ocr_locale()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
