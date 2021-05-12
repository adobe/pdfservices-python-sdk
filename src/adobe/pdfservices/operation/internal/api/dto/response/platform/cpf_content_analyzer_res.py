# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import json

from adobe.pdfservices.operation.internal.api.dto.response.extract_pdf_output_metadata import ExtractPDFOutputMetadata
from adobe.pdfservices.operation.internal.api.dto.response.platform.cpf_status import CPFStatus
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder, JSONHintDecoder


class ExtractContentAnalyzerResponse(json.JSONDecoder):

    json_hint = {
        'status': {'name' : 'cpf:status', 'type' : CPFStatus },
        'outputs': { 'name' : 'cpf:outputs', 'type' : ExtractPDFOutputMetadata}
    }

    def __init__(self, outputs : ExtractPDFOutputMetadata = None, status : CPFStatus = None):
        self.outputs = outputs
        self.status = status

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=4, sort_keys=True)

    @staticmethod
    def from_json( json_str):
        JSONHintDecoder.current_class = ExtractContentAnalyzerResponse
        return JSONHintDecoder.as_class(json.loads(json_str))
