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
import mimetypes

from adobe.pdfservices.operation.internal.api.dto.document import Document
from adobe.pdfservices.operation.internal.api.dto.request.platform.outputs import Outputs
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants


#TODO Why did it require JSONDecoder?
class ExtractPDFOutputs(Outputs, json.JSONDecoder):

    json_hint = {
        'elements_info_format' : {'name' : 'elementsInfo', 'type' : Document},
        'elements_renditions_format' : { 'name' : 'elementsRenditions', 'type' : Document}
    }
    # Why is this type definition required
    elements_info : Document
    elements_renditions : Document

    def __init__(self):
        super().__init__()
        self.elements_info_format = Document(mimetypes.types_map['.json'], "jsonoutput")
        self.elements_renditions_format = Document(ServiceConstants.TEXT_MIME_TYPE, "fileoutpart")
