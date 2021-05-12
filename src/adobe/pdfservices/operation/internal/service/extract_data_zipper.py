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
import zipfile


class ExtractDataZipper:
    zip_file = None

    def __init__(self, file_path):
        self.zip_file = zipfile.ZipFile(file_path, mode='w')

    rdata = []

    def add_structured_data(self, data):
        self.zip_file.writestr(data= json.dumps(data.data), zinfo_or_arcname= data.get_file_name())

    def add_rendition_data(self, rdata):
        file_name = rdata.file_name + rdata.rendition_extension
        folder_name = "renditions"
        if not file_name:
            file_name = "random"

        if rdata.pdf_element_type:
            folder_name  = rdata.pdf_element_type.lower()
        file_name = os.path.join(folder_name, file_name)
        self.zip_file.writestr(data= rdata.body, zinfo_or_arcname= file_name)
