# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
import json
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder

from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions
from adobe.pdfservices.operation.internal.api.dto.request.platform.platform_api_request import PlatformApiRequest


class AutotagPDFRequest(PlatformApiRequest):
    json_hint = {
        'asset_id': 'assetID',
        'generate_report': 'generateReport',
        'shift_headings': 'shiftHeadings'
    }

    def __init__(self, asset_id: str= None, generate_report: bool = None, shift_headings: bool = None):
        super().__init__()
        self.asset_id = asset_id
        self.generate_report = generate_report
        self.shift_headings = shift_headings

    @classmethod
    def from_autotag_pdf_options(cls, asset_id, autotag_pdf_options: AutotagPDFOptions = None):
        if autotag_pdf_options is None:
            return cls(asset_id=asset_id)
        return cls(asset_id=asset_id,generate_report=autotag_pdf_options.generate_report,
                   shift_headings=autotag_pdf_options.shift_headings)

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
