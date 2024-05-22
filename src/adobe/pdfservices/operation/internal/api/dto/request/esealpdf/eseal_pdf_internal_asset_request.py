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
from adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params import PDFElectronicSealParams


class ESealPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'input_document_asset_id': 'inputDocumentAssetID',
        'seal_image_asset_id': 'sealImageAssetID',
        'seal_options': 'sealOptions',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_document_asset_id: str, seal_image_asset_id: str,
                 electronic_seal_params: PDFElectronicSealParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.input_document_asset_id = input_document_asset_id
        self.notify_config_list = notify_config_list
        self.seal_image_asset_id = seal_image_asset_id
        self.seal_options = electronic_seal_params.to_dict()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
