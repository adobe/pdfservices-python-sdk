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
from abc import ABC
from typing import List

from adobe.pdfservices.operation.config.notifier.notifier_config import NotifierConfig
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import \
    PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.pdfjobs.params.pdf_accessibility_checker.pdf_accessibility_checker_params import \
    PDFAccessibilityCheckerParams


class PDFAccessibilityCheckerInternalAssetRequest(PDFServicesAPIRequest, ABC):
    json_hint = {
        'asset_id': 'assetID',
        'page_start': 'pageStart',
        'page_end': 'pageEnd',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id: str, pdf_accessibility_checker_params: PDFAccessibilityCheckerParams = None,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = asset_id
        if pdf_accessibility_checker_params is not None:
            self.page_start = pdf_accessibility_checker_params.get_page_start()
            self.page_end = pdf_accessibility_checker_params.get_page_end()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
