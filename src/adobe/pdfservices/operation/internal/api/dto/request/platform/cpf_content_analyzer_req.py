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

from adobe.pdfservices.operation.internal.api.dto.request.platform.engine import Engine
from adobe.pdfservices.operation.internal.api.dto.request.platform.inputs import Inputs
from adobe.pdfservices.operation.internal.api.dto.request.platform.outputs import Outputs
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class CPFContentAnalyzerRequests:

    json_hint = {
        'engine' : 'cpf:engine',
        'inputs' : 'cpf:inputs',
        'outputs' : 'cpf:outputs'
    }

    def __init__(self, service_id, inputs: Inputs, outputs : Outputs):
        self.engine = Engine(service_id)
        self.inputs = inputs
        self.outputs = outputs

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=4, sort_keys=True)