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
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_pdf_params import ExtractPDFParams


class ExtractPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'get_char_bounds': 'getCharBounds',
        'include_styling': 'includeStyling',
        'elements_to_extract': 'elementsToExtract',
        'table_output_format': 'tableOutputFormat',
        'renditions_to_extract': 'renditionsToExtract',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset_id: str, extract_pdf_params: ExtractPDFParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = input_asset_id
        if extract_pdf_params is not None:
            self.get_char_bounds = extract_pdf_params.get_add_char_info() \
                if extract_pdf_params.get_add_char_info() is not None else None
            self.include_styling = extract_pdf_params.get_styling_info() \
                if extract_pdf_params.get_styling_info() is not None else None
            self.elements_to_extract = extract_pdf_params.get_elements_to_extract() \
                if extract_pdf_params.get_elements_to_extract() is not None else None
            self.table_output_format = extract_pdf_params.get_table_structure_type().__str__() \
                if extract_pdf_params.get_table_structure_type() is not None else None
            self.renditions_to_extract = extract_pdf_params.get_elements_to_extract_renditions() \
                if extract_pdf_params.get_elements_to_extract_renditions() is not None else None
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
