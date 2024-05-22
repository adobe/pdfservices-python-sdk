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
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.html_to_pdf_params import HTMLtoPDFParams


class HTMLtoPDFParamsPayload:
    json_hint = {
        'json': 'json',
        'include_header_footer': 'includeHeaderFooter',
        'page_layout': 'pageLayout'
    }

    def __init__(self, html_to_pdf_params: HTMLtoPDFParams):
        self.json = html_to_pdf_params.get_json()
        self.include_header_footer = html_to_pdf_params.get_include_header_footer()
        self.page_layout = html_to_pdf_params.get_page_layout()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
