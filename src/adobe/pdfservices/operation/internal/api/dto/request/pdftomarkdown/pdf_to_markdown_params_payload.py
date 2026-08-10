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
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_markdown.pdf_to_markdown_params import PDFToMarkdownParams


class PDFToMarkdownParamsPayload:
    json_hint = {
        'get_figures': 'getFigures'
    }

    def __init__(self, pdf_to_markdown_params: PDFToMarkdownParams):
        self.get_figures = False
        if pdf_to_markdown_params is not None:
            self.get_figures = pdf_to_markdown_params.get_figures()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)

