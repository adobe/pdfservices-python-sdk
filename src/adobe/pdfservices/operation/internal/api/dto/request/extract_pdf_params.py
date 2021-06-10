# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
from typing import List

from adobe.pdfservices.operation.internal.api.dto.request.platform.inline_params import InlineParams
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions


class ExtractPDFParams(InlineParams):
    json_hint = {
        'elements_to_extract': 'elementsToExtract',
        'renditions_to_extract': 'renditionsToExtract',
        'table_output_format': 'tableOutputFormat',
        'extract_char_info': 'getCharBounds',
        'include_styling_info': 'includeStyling'
    }

    def __init__(self, elements_to_extract: List[ExtractElementType] = None,
                 renditions_to_extract: List[ExtractRenditionsElementType] = None, table_output_format: TableStructureType = None,
                 extract_char_info: bool = None, include_styling_info: bool = None):
        super().__init__()
        self.elements_to_extract = elements_to_extract
        self.renditions_to_extract = renditions_to_extract
        self.table_output_format = table_output_format
        self.extract_char_info = extract_char_info
        self.include_styling_info = include_styling_info

    @classmethod
    def from_extract_pdf_options(cls, extract_pdf_options: ExtractPDFOptions = None):
        if extract_pdf_options:
            return cls(elements_to_extract=extract_pdf_options.elements_to_extract,
                       renditions_to_extract=extract_pdf_options.elements_to_extract_renditions,
                       table_output_format=extract_pdf_options.table_output_format,
                       extract_char_info=extract_pdf_options.get_char_info,
                       include_styling_info=extract_pdf_options.include_styling_info)
        else:
            return cls(elements_to_extract=[ExtractElementType.TEXT])

    def to_json(self):
        pass
