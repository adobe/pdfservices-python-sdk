# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
from adobe.pdfservices.operation.io.file_ref import FileRef


class AutotagPDFOutputFiles:

    def __init__(self):
        self._pdf_file: FileRef = None
        self._xls_file: FileRef = None

    @property
    def pdf_file(self):
        return self._pdf_file

    @property
    def xls_file(self):
        return self._xls_file

    @pdf_file.setter
    def pdf_file(self, pdf_file):
        self._pdf_file = pdf_file

    @xls_file.setter
    def xls_file(self, xls_file):
        self._xls_file = xls_file
