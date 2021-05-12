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

from adobe.pdfservices.operation.internal.api.dto.document import Document


class ExtractPDFOutputMetadata(json.JSONDecoder):

    json_hint = {
        'elements_info_format' : {'name' : 'elementsInfo', 'type' : Document},
        'elements_renditions_format' : { 'name' : 'elementsRenditions', 'type' : Document}
    }

    elements_info_format : Document
    elements_renditions_format : [Document]
    indexed_meta_info = {}

    def parse_indexed_metadata(self):
        if self.elements_info_format:
            self.indexed_meta_info[self.elements_info_format.location] = self.elements_info_format

        if self.elements_renditions_format:
            for rendition in self.elements_renditions_format:
                self.indexed_meta_info[rendition.location] = rendition

    def __init__(self, elements_info_format : Document = None, elements_renditions_format : [Document] = None):
        self.elements_info_format = elements_info_format
        self.elements_renditions_format = elements_renditions_format

    def post_process(self):
        self.parse_indexed_metadata()

    def to_json(self):
        pass