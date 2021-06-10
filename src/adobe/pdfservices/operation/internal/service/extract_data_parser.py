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
import os
import mimetypes

from requests_toolbelt import MultipartDecoder

from adobe.pdfservices.operation.internal.api.dto.response.extract_pdf_output_metadata import ExtractPDFOutputMetadata
from adobe.pdfservices.operation.internal.api.dto.response.platform.cpf_content_analyzer_res import \
    ExtractContentAnalyzerResponse
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.service.extract_data_zipper import ExtractDataZipper
from adobe.pdfservices.operation.internal.service.rendition_output import ExtractRenditionOutput


class StructuredData:
    file_format: str
    data: str
    elementContentNameToType: dict = {}
    renditionToPathMapping = {"TABLES": "table",
                              "FIGURES": "figure"}

    def __init__(self, file_format, data):
        self.file_format = file_format
        self.data = data
        self.parse_data()

    def get_pdfelement_type(self, filename):
        if filename.find(":") >= 0:
            filename = filename.split(":")[1]
        return self.elementContentNameToType.get(filename, "renditions")

    def parse_data(self):
        if "elements" in self.data:
            self.update_elements_path_for_tables_and_renditions(self.data["elements"])

    def update_elements_path_for_tables_and_renditions(self, elements):
        for element in elements:
            rendition_type = self.pdf_rendition_identifier(element)
            if rendition_type:
                fileNames = element["filePaths"]
                for idx, fileName in enumerate(fileNames):
                    self.elementContentNameToType[fileName] = rendition_type
                    fileNames[idx] = "{dir}{path_sep}{file_name}".format(dir=rendition_type.lower(),
                                                                         path_sep=os.path.sep,
                                                                         file_name=fileName)
            # Kids is a list of elements which is present if styling info is included
            Kids = element.get("Kids", [])
            if len(Kids) > 0:
                self.update_elements_path_for_tables_and_renditions(Kids)


    def pdf_rendition_identifier(self, pdf_element):
        if self.is_rendition_element(pdf_element):
            identifier = pdf_element["Path"].rsplit("/", 1)[1]
            for key, value in self.renditionToPathMapping.items():
                if identifier.lower().startswith(value.lower()):
                    return key
        return None

    def is_rendition_element(self, pdf_element):
        if pdf_element and "filePaths" in pdf_element and "Path" in pdf_element:
            return len(pdf_element["filePaths"]) > 0 and pdf_element["Path"]
        return False

    def get_file_name(self):
        return "structuredData" + self.file_format


class MultiPartKey:
    contentAnalyzerResponse: str
    jsonoutput: str
    rendition: []

    def __init__(self):
        self.contentAnalyzerResponse = ''
        self.jsonoutput = ''
        self.rendition = []


class ExtractDataParser:
    content: str = None
    content_type_header: str = None
    zip_file_path = ''
    ed_zipper: ExtractDataZipper

    def __init__(self, content, content_type_header, file_path):
        self.content = content
        self.content_type_header = content_type_header
        self.zip_file_path = file_path
        self.ed_zipper = ExtractDataZipper(file_path)

    @staticmethod
    def get_key_dstring(cds):
        if cds.startswith(b'form-data'):
            cds = cds.decode()
            return cds.replace("form-data; name=\"", "").replace("\"", "")

    @staticmethod
    def filename_with_extension(file_name, extension):
        if extension:
            file_name += extension
        return file_name

    @staticmethod
    def get_extension(file_format):
        return mimetypes.guess_extension(file_format)

    def frame_extract_rendition_output(self,
                                       extract_output_metadata: ExtractPDFOutputMetadata,
                                       structured_data: StructuredData,
                                       body_part,
                                       file_name
                                       ):
        ero: ExtractRenditionOutput = ExtractRenditionOutput()
        ero.file_name = file_name
        ero.body = body_part
        file_format = extract_output_metadata.indexed_meta_info[file_name].dc_format
        ero.rendition_extension = ExtractDataParser.get_extension(file_format)
        ero.pdf_element_type = structured_data.get_pdfelement_type(
            ExtractDataParser.filename_with_extension(file_name, ero.rendition_extension))
        return ero

    def get_output_metadata(self, analyzer_str):
        pass

    @staticmethod
    def get_keys(key_to_content_map: map):
        multipart_key = MultiPartKey()
        for key in key_to_content_map.keys():
            if ServiceConstants.CONTENT_ANALYZER_RESPONSE_STRING in key:
                multipart_key.contentAnalyzerResponse = key
            elif 'jsonoutput' in key:
                multipart_key.jsonoutput = key
            else:
                multipart_key.rendition.append(key)
        return multipart_key

    def parse(self):

        decoded_content = MultipartDecoder(self.content,
                                           self.content_type_header)
        key_to_content_map = {}
        for part in decoded_content.parts:
            cds = part.headers[b'Content-Disposition']
            key = ExtractDataParser.get_key_dstring(cds)
            key_to_content_map[key] = part.content

        # For Json Response
        keys: MultiPartKey = ExtractDataParser.get_keys(key_to_content_map)
        extract_json = key_to_content_map[keys.contentAnalyzerResponse].decode()
        extract_content_analyzer_res = ExtractContentAnalyzerResponse.from_json(extract_json)
        extract_output_metadata: ExtractPDFOutputMetadata = extract_content_analyzer_res.outputs

        # For ElementsInfo
        structured_output = key_to_content_map[keys.jsonoutput].decode()
        mt = mimetypes.MimeTypes()
        extension = mt.guess_extension(extract_output_metadata.indexed_meta_info[keys.jsonoutput].dc_format)
        structure_output: StructuredData = StructuredData(
            extension,
            json.loads(structured_output))
        self.ed_zipper.add_structured_data(structure_output)

        # For Elements Renditions
        for rendition_key in keys.rendition:
            rendition_output: ExtractRenditionOutput = self.frame_extract_rendition_output(
                extract_output_metadata,
                structure_output,
                key_to_content_map[rendition_key],
                rendition_key)
            self.ed_zipper.add_rendition_data(rendition_output)
