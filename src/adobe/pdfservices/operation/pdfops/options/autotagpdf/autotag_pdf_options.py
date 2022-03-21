# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from adobe.pdfservices.operation.pdfops.options.autotagpdf.pdf_version import PdfVersion


class AutotagPDFOptions():
    """ An Options Class that defines the options for AutotagPDFOperation.

    .. code-block:: python

        autotag_pdf_options: AutotagPDFOptions = AutotagPDFOptions.builder() \\
            .generate_report() \\
            .shift_headings() \\
            .pdf_version(PDFVersion.v17,PDFVersion.V20) \\
            .build()

    """

    def __init__(self, generate_report, pdf_version, shift_headings):
        self._generate_report = generate_report
        self._pdf_version = pdf_version
        self._shift_headings = shift_headings

    @property
    def generate_report(self):
        """ Boolean specifying whether to generate report containing information of the tags"""
        return self._generate_report

    @property
    def pdf_version(self):
        """ The version of the output tagged pdf"""
        return self._pdf_version

    @property
    def shift_headings(self):
        """ Boolean specifying whether to shift headings of the pdf """
        return self._shift_headings

    def get_generate_report(self):
        """" returns the boolean value of generate report parameter """
        return self.generate_report

    @staticmethod
    def builder():
        """Returns a Builder for :class:`AutotagPDFOptions`

        :return: The builder class for AutotagPDFOptions
        :rtype: AutotagPDFOptions.Builder
        """
        return AutotagPDFOptions.Builder()

    class Builder:
        """ The builder for :class:`AutotagPDFOptions`.
        """

        def __init__(self):
            self._generate_report = False
            self._pdf_version = None
            self._shift_headings = False

        def with_pdf_version(self, pdf_version: PdfVersion):
            """
            determines the pdf version of the tagged pdf will be 1.7 or 2.0

            :param pdf_version: PdfVersion to be extracted
            :type pdf_version: PdfVersion
            :return: This Builder instance to add any additional parameters.
            :rtype: AutotagPDFOptions.Builder
            :raises ValueError: if pdf_version is None.
            """
            if pdf_version and pdf_version in PdfVersion:
                self._pdf_version = pdf_version
            else:
                raise ValueError("Only PdfVersion enum is accepted for pdf_version_format")
            return self

        def with_generate_report(self):
            """
            sets the Boolean specifying whether to output an excel report containing the information of the tags

            :param generate_report: Set True to generate report containing the information of the tags
            :type generate_report: bool
            :return: This Builder instance to add any additional parameters.
            :rtype: AutotagPDFOptions.Builder
            """
            self._generate_report = True
            return self

        def with_shift_headings(self):
            """
            sets the Boolean specifying whether to shift headings of the pdf

            :param shift_headings: Set True to shift headings of the pdf
            :type shift_headings: bool
            :return: This Builder instance to add any additional parameters.
            :rtype: AutotagPDFOptions.Builder
            """
            self._shift_headings = True
            return self

        def build(self):
            return AutotagPDFOptions(self._generate_report, self._pdf_version,
                                     self._shift_headings)
