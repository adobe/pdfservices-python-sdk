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
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.pdfjobs.params.import_pdf_form_data.import_pdf_form_data_params import ImportPDFFormDataParams


class ImportPDFFormDataParamsPayload:
    """
    Payload class for Import PDF Form Data parameters
    """
    json_hint = {
        'json_form_fields_data': 'jsonFormFieldsData'
    }

    def __init__(self, import_pdf_form_data_params: ImportPDFFormDataParams = None):
        """
        Constructs a new ImportPDFFormDataParamsPayload instance.

        :param import_pdf_form_data_params: Parameters containing form data to import
        :type import_pdf_form_data_params: ImportPDFFormDataParams
        """
        self.json_form_fields_data = None
        if import_pdf_form_data_params is not None:
            self.json_form_fields_data = import_pdf_form_data_params.get_json_form_fields_data()

    def to_json(self):
        """
        :return: JSON representation of the payload
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)


class ImportPDFFormDataExternalAssetRequest(PDFServicesAPIRequest):
    """
    Request DTO for Import PDF Form Data operation using external assets
    """
    
    json_hint = {
        'input_asset': 'input',
        'params': 'params',
        'output_asset': 'output',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, input_asset: ExternalAsset, import_pdf_form_data_params: ImportPDFFormDataParams,
                 notifier_config_list: List[NotifierConfig] = None):
        """
        Constructs a new ImportPDFFormDataExternalAssetRequest instance.

        :param input_asset: External asset representing the input PDF
        :type input_asset: ExternalAsset
        :param import_pdf_form_data_params: Parameters containing form data to import
        :type import_pdf_form_data_params: ImportPDFFormDataParams
        :param notifier_config_list: List of notifier configurations (Optional)
        :type notifier_config_list: List[NotifierConfig]
        """
        super().__init__()
        self.input_asset = input_asset
        self.params = ImportPDFFormDataParamsPayload(import_pdf_form_data_params)
        self.notify_config_list = notifier_config_list
        self.output_asset = None

    def set_output(self, output_asset: ExternalAsset):
        """
        Sets the output external asset.

        :param output_asset: External asset for output
        :type output_asset: ExternalAsset
        :return: Self for method chaining
        :rtype: ImportPDFFormDataExternalAssetRequest
        """
        self.output_asset = output_asset
        return self

    def to_json(self):
        """
        :return: JSON representation of the request
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True) 