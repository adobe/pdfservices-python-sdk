# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.


class AutotagPDFOptions():
    """ An Options Class that defines the options for AutotagPDFOperation.

    .. code-block:: python

        autotag_pdf_options: AutotagPDFOptions = AutotagPDFOptions.builder() \\
            .generate_report() \\
            .shift_headings() \\
            .build()
    """

    def __init__(self, generate_report, shift_headings):
        self._generate_report = generate_report
        self._shift_headings = shift_headings

    @property
    def generate_report(self):
        """ Boolean specifying whether to generate an XLSX report as an output"""
        return self._generate_report

    @property
    def shift_headings(self):
        """ Boolean specifying whether to shift the headings in the output PDF file """
        return self._shift_headings

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
            self._shift_headings = False

        def with_generate_report(self):
            """
            sets the Boolean specifying whether to generate an XLSX report containing the information about the tags

            :return: This Builder instance to add any additional parameters.
            :rtype: AutotagPDFOptions.Builder
            """
            self._generate_report = True
            return self

        def with_shift_headings(self):
            """
            sets the Boolean specifying whether to shift headings in the output PDF file

            :return: This Builder instance to add any additional parameters.
            :rtype: AutotagPDFOptions.Builder
            """
            self._shift_headings = True
            return self

        def build(self):
            """builds and returns the AutotagPDFOptions instance"""
            return AutotagPDFOptions(self._generate_report, self._shift_headings)
