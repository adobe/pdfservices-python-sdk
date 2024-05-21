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
from adobe.pdfservices.operation.pdfjobs.params.create_pdf.CreatePDFParams import CreatePDFParams


class CreatePDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'document_language': 'documentLanguage',
        'create_tagged_pdf': 'createTaggedPDF',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id, create_pdf_params: CreatePDFParams, notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = asset_id
        self.notify_config_list = notify_config_list
        self.create_tagged_pdf = False
        if create_pdf_params is not None:
            self.document_language = create_pdf_params.get_document_language().get_document_language()
            self.create_tagged_pdf = create_pdf_params.get_create_tagged_pdf()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
