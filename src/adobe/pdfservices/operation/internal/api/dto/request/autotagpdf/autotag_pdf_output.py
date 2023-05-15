# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
from logging import getLogger

from adobe.pdfservices.operation.io.file_ref import FileRef

logger = getLogger(__name__)


class AutotagPDFOutput:
    """
    Class for providing support for output files namely tagged PDF and XLSX report file for AutotagPDFOperation
    """

    def __init__(self, tagged_pdf: FileRef = None, report: FileRef = None):
        self._tagged_pdf = tagged_pdf
        self._report = report

    @property
    def tagged_pdf(self):
        return self._tagged_pdf

    @property
    def report(self):
        return self._report

    def get_tagged_pdf(self):
        return self._tagged_pdf

    def get_report(self):
        return self._report
