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
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.html_to_pdf_params import HTMLtoPDFParams


class HTMLtoPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'input_url': 'inputUrl',
        'json': 'json',
        'include_header_footer': 'includeHeaderFooter',
        'page_layout': 'pageLayout',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset_id, input_url, html_to_pdf_params: HTMLtoPDFParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        if input_asset_id is not None:
            self.asset_id = input_asset_id
        if input_url is not None:
            self.input_url = input_url
        if html_to_pdf_params is not None:
            self.json = html_to_pdf_params.get_json()
            self.include_header_footer = html_to_pdf_params.get_include_header_footer()
            self.page_layout = html_to_pdf_params.get_page_layout()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
