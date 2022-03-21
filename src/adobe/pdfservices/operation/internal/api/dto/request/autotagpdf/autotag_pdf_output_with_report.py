# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import json
from json import JSONDecoder

from adobe.pdfservices.operation.internal import extension_media_type_mapping
from adobe.pdfservices.operation.internal.api.dto.document import Document
from adobe.pdfservices.operation.internal.api.dto.request.platform.outputs import Outputs
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping


#TODO Why did it require JSONDecoder?
class AutotagPDFOutputWithReport(Outputs, json.JSONDecoder):

    json_hint = {
        'elements_pdf_format' : {'name' : 'tagged-pdf', 'type' : Document},
        'elements_xls_format' : { 'name' : 'report', 'type' : Document}
    }


    def __init__(self):
        super().__init__()
        self.elements_pdf_format = Document(ExtensionMediaTypeMapping.PDF, "taggedoutput")
        self.elements_xls_format = Document(ExtensionMediaTypeMapping.XLSX, "reportoutput")

