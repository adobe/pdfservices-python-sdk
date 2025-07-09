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
from adobe.pdfservices.operation.internal.api.dto.request.pdf_services_api.pdf_services_api_request import PDFServicesAPIRequest
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.pdfjobs.params.import_pdf_form_data.import_pdf_form_data_params import ImportPDFFormDataParams


class ImportPDFFormDataInternalAssetRequest(PDFServicesAPIRequest):
    """
    Request DTO for Import PDF Form Data operation using internal assets
    """
    
    json_hint = {
        'asset_id': 'assetID',
        'json_form_fields_data': 'jsonFormFieldsData',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id: str, import_pdf_form_data_params: ImportPDFFormDataParams,
                 notifier_config_list: List[NotifierConfig] = None):
        """
        Constructs a new ImportPDFFormDataInternalAssetRequest instance.

        :param asset_id: Asset ID of the input PDF document
        :type asset_id: str
        :param import_pdf_form_data_params: Parameters containing form data to import
        :type import_pdf_form_data_params: ImportPDFFormDataParams
        :param notifier_config_list: List of notifier configurations (Optional)
        :type notifier_config_list: List[NotifierConfig]
        """
        super().__init__()
        self.asset_id = asset_id
        self.json_form_fields_data = import_pdf_form_data_params.get_json_form_fields_data()
        self.notify_config_list = notifier_config_list

    def to_json(self):
        """
        :return: JSON representation of the request
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True) 