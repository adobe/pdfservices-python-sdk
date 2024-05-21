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

from adobe.pdfservices.operation.internal.api.dto.response.pdf_services_api.job_error_response import JobErrorResponse
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder, JSONHintDecoder


class PDFServicesAPIResponse:
    json_hint = {
        'status': 'status',
        'error': 'error'
    }

    def __init__(self, status: int, error: JobErrorResponse):
        self.error = error
        self.status = status

    def get_error_response(self):
        return self.error

    def get_status(self):
        return self.status

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=4, sort_keys=True)

    @staticmethod
    def from_json(json_str):
        JSONHintDecoder.current_class = PDFServicesAPIResponse
        return JSONHintDecoder.as_class(json.loads(json_str))
