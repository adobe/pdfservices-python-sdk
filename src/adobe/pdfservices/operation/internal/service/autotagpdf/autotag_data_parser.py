# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from requests_toolbelt import MultipartDecoder

from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_output_files import \
    AutotagPDFOutputFiles
from adobe.pdfservices.operation.io.file_ref import FileRef


class AutotagDataParser:
    content: str = None
    content_type_header: str = None
    pdf_file_path: FileRef
    xls_file_path: FileRef

    def __init__(self, content, content_type_header, pdf_file_path, xls_file_path):
        self.content = content
        self.content_type_header = content_type_header
        self.pdf_file_path = pdf_file_path
        self.xls_file_path = xls_file_path

    @staticmethod
    def get_key_dstring(cds):
        if cds.startswith(b'form-data'):
            cds = cds.decode()
            return cds.replace("form-data; name=\"", "").replace("\"", "")

    def save_file(self, body, filename):
        if 'taggedoutput' in filename:
            file_path = self.pdf_file_path
        elif 'reportoutput' in filename:
            file_path = self.xls_file_path
        else:
            return
        with open(file_path, 'wb') as file:
            file.write(body)

    def parse(self):
        decoded_content = MultipartDecoder(self.content,
                                           self.content_type_header)
        for part in decoded_content.parts:
            cds = part.headers[b'Content-Disposition']
            key = AutotagDataParser.get_key_dstring(cds)
            self.save_file(part.content, key)

        autotag_pdf_output_files = AutotagPDFOutputFiles()
        autotag_pdf_output_files.pdf_file = self.pdf_file_path
        autotag_pdf_output_files.xls_file = self.xls_file_path
        return autotag_pdf_output_files
