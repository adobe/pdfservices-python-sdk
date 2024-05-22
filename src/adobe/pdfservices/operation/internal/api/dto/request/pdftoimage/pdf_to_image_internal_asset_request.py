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
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_params import \
    ExportPDFtoImagesParams


class PDFToImagesInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'target_format': 'targetFormat',
        'output_type': 'outputType',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset_id: str, export_pdf_to_images_params: ExportPDFtoImagesParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = input_asset_id
        self.target_format = export_pdf_to_images_params.get_export_pdf_to_images_target_format().get_file_ext()
        self.output_type = export_pdf_to_images_params.get_export_pdf_to_images_output_type().get_output_type()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
