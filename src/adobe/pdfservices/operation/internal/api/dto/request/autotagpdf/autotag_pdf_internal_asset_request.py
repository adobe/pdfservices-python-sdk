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
from adobe.pdfservices.operation.pdfjobs.params.autotag_pdf.autotag_pdf_params import AutotagPDFParams


class AutotagPDFInternalAssetRequest(PDFServicesAPIRequest, ABC):
    json_hint = {
        'asset_id': 'assetID',
        'shift_headings': 'shiftHeadings',
        'generate_report': 'generateReport',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id: str, autotag_pdf_params: AutotagPDFParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = asset_id
        if autotag_pdf_params is not None:
            self.shift_headings = autotag_pdf_params.get_shift_headings()
            self.generate_report = autotag_pdf_params.get_generate_report()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
