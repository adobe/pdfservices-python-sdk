# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
from adobe.pdfservices.operation.internal.api.dto.document import Document
from adobe.pdfservices.operation.internal.api.dto.request.platform.cpf_params import CPFParams



class Inputs:

    json_hint = {
        'document_in' : 'documentIn',
        'params' : 'params',
    }

    def __init__(self, input_file_format, params: CPFParams):
        self.document_in = Document(input_file_format, 'fileInput1')
        self.params = params

    def to_json(self):
        pass