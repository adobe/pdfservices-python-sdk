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
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params import PDFElectronicSealParams


class ESealPDFExternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'inputs': 'inputs',
        'output': 'output',
        'params': 'params',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset: Asset,
                 electronic_seal_params: PDFElectronicSealParams,
                 seal_image_asset: Asset = None,
                 notify_config_list: List[NotifierConfig] = None,
                 output_asset: ExternalAsset = None):
        super().__init__()
        self.inputs = {'document': input_asset}
        if seal_image_asset is not None:
            self.inputs['sealImage'] = seal_image_asset
        self.params = {
            'sealOptions': electronic_seal_params.to_dict()
        }
        if output_asset is not None:
            self.output = output_asset
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
