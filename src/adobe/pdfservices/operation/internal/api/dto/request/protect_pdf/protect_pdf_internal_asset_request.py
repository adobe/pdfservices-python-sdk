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
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.password_protect_params import PasswordProtectParams


class ProtectPDFInternalAssetRequest(PDFServicesAPIRequest):
    json_hint = {
        'asset_id': 'assetID',
        'password_protection': 'passwordProtection',
        'encryption_algorithm': 'encryptionAlgorithm',
        'content_to_encrypt': 'contentToEncrypt',
        'permissions': 'permissions',
        'notify_config_list': 'notifiers'
    }

    def __init__(self, asset_id: str, protect_pdf_params: PasswordProtectParams,
                 notify_config_list: List[NotifierConfig] = None):
        super().__init__()
        self.asset_id = asset_id

        password_protection = {}
        if protect_pdf_params.get_user_password() is not None:
            password_protection['userPassword'] = protect_pdf_params.get_user_password()
        if protect_pdf_params.get_owner_password() is not None:
            password_protection['ownerPassword'] = protect_pdf_params.get_owner_password()
        if protect_pdf_params.get_permissions() is not None:
            self.permissions = protect_pdf_params.get_permissions().get_values()
        if protect_pdf_params.get_content_encryption() is not None:
            self.content_to_encrypt = protect_pdf_params.get_content_encryption().__str__()

        self.password_protection = password_protection
        self.encryption_algorithm = protect_pdf_params.get_encryption_algorithm().__str__()
        self.notify_config_list = notify_config_list

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
