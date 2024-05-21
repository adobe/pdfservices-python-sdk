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
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.document_merge_params import DocumentMergeParams


class DocumentMergeInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'output_format': 'outputFormat',
        'json_data_for_merge': 'jsonDataForMerge',
        'fragments': 'fragments',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id: str, document_merge_params: DocumentMergeParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = asset_id
        self.notify_config_list = notify_config_list
        self.output_format = document_merge_params.get_output_format().get_format()
        self.json_data_for_merge = document_merge_params.get_json_data_for_merge()
        if document_merge_params.get_fragments() is not None:
            self.fragments = document_merge_params.get_fragments().get_fragments_list()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
