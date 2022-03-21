# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from adobe.pdfservices.operation.internal.api.dto.request.platform.inline_params import InlineParams
from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions
from adobe.pdfservices.operation.pdfops.options.autotagpdf.pdf_version import PdfVersion


class AutotagPDFParams(InlineParams):
    json_hint = {
        'pdf_version': 'pdfVersion',
        'generate_report': 'generateReport',
        'shift_headings': 'shiftHeadings'
    }

    def __init__(self, pdf_version: PdfVersion,
                 generate_report: bool = None, shift_headings: bool = None):
        super().__init__()
        self.pdf_version = pdf_version
        self.generate_report = generate_report
        self.shift_headings = shift_headings

    @classmethod
    def from_autotag_pdf_options(cls, autotag_pdf_options: AutotagPDFOptions = None):
            return cls(pdf_version=autotag_pdf_options.pdf_version,
                       generate_report=autotag_pdf_options.generate_report,
                       shift_headings=autotag_pdf_options.shift_headings)
    def to_json(self):
        raise NotImplementedError("The Function to_json is not implemented")
