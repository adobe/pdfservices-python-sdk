# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
from typing import List

from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType


class ExtractPDFOptions():
    """ An Options Class that defines the options for ExtractPDFOperation.

    .. code-block:: python

        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \\
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \\
            .with_get_char_info(True) \\
            .with_table_structure_format(TableStructureType.CSV) \\
            .with_elements_to_extract_renditions([ExtractRenditionsElementType.FIGURES, ExtractRenditionsElementType.TABLES]) \\
            .with_include_styling_info(True) \\
            .build()

    """

    def __init__(self, elements_to_extract, elements_to_extract_renditions, get_char_info, table_output_format,
                 include_styling_info=None):
        self._elements_to_extract = elements_to_extract
        self._elements_to_extract_renditions = elements_to_extract_renditions
        self._get_char_info = get_char_info
        self._table_output_format = table_output_format
        self._include_styling_info = include_styling_info
        self._logger = logging.getLogger(__name__)

    @property
    def elements_to_extract(self):
        """ List of pdf element types to be extracted in a structured format from input file"""
        return self._elements_to_extract

    @property
    def elements_to_extract_renditions(self):
        """ List of pdf element types whose renditions needs to be extracted from input file"""
        return self._elements_to_extract_renditions

    @property
    def get_char_info(self):
        """ Boolean specifying whether to add character level bounding boxes to output json """
        return self._get_char_info

    @property
    def table_output_format(self):
        """ export table in specified format - currently csv supported """
        return self._table_output_format

    @property
    def include_styling_info(self):
        """ Boolean specifying whether to add PDF Elements Styling Info to output json """
        return self._include_styling_info

    @staticmethod
    def builder():
        """Returns a Builder for :class:`ExtractPDFOptions`

        :return: The builder class for ExtractPDFOptions
        :rtype: ExtractPDFOptions.Builder
        """
        return ExtractPDFOptions.Builder()

    class Builder:
        """ The builder for :class:`ExtractPDFOptions`.
        """

        def __init__(self):
            self._elements_to_extract = None
            self._elements_to_extract_renditions = None
            self._table_output_format = None
            self._get_char_info = None
            self._include_styling_info = None

        def _init_elements_to_extract(self):
            if not self._elements_to_extract:
                self._elements_to_extract = []

        def _init_elements_to_extract_renditions(self):
            if not self._elements_to_extract_renditions:
                self._elements_to_extract_renditions = []

        def with_element_to_extract(self, element_to_extract: ExtractElementType):
            """
            adds a pdf element type for extracting structured information.

            :param element_to_extract: ExtractElementType to be extracted
            :type element_to_extract: ExtractElementType
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            :raises ValueError: if element_to_extract is None.
            """
            if element_to_extract and element_to_extract in ExtractElementType:
                self._init_elements_to_extract()
                self._elements_to_extract.append(element_to_extract)
            else:
                raise ValueError("Only ExtractElementType enum is accepted for element_to_extract")
            return self

        def with_elements_to_extract(self, elements_to_extract: List[ExtractElementType]):
            """
            adds a list of pdf element types for extracting structured information.

            :param elements_to_extract: List of ExtractElementType to be extracted
            :type elements_to_extract: List[ExtractElementType]
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            :raises ValueError: if elements_to_extract is None or empty list.
            """
            if elements_to_extract and all(element in ExtractElementType for element in elements_to_extract):
                self._init_elements_to_extract()
                self._elements_to_extract.extend(elements_to_extract)
            else:
                raise ValueError("Only ExtractElementType enum List is accepted for elements_to_extract")
            return self

        def with_element_to_extract_renditions(self, element_to_extract_renditions: ExtractRenditionsElementType):
            """
            adds a pdf element type for extracting rendition.

            :param element_to_extract_renditions: ExtractRenditionsElementType whose renditions have to be extracted
            :type element_to_extract_renditions: ExtractRenditionsElementType
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            :raises ValueError: if element_to_extract_renditions is None.
            """
            if element_to_extract_renditions and element_to_extract_renditions in ExtractRenditionsElementType:
                self._init_elements_to_extract_renditions()
                self._elements_to_extract_renditions.append(element_to_extract_renditions)
            else:
                raise ValueError("Only ExtractRenditionsElementType enum is accepted for element_to_extract_renditions")
            return self

        def with_elements_to_extract_renditions(self, elements_to_extract_renditions: List[ExtractRenditionsElementType]):
            """
            adds a list of pdf element types for extracting rendition.

            :param elements_to_extract_renditions: List of ExtractRenditionsElementType whose renditions have to be extracted
            :type elements_to_extract_renditions: List[ExtractRenditionsElementType]
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            :raises ValueError: if elements_to_extract is None or empty list.
            """
            if elements_to_extract_renditions and all(
                    element in ExtractRenditionsElementType for element in elements_to_extract_renditions):
                self._init_elements_to_extract_renditions()
                self._elements_to_extract_renditions.extend(elements_to_extract_renditions)
            else:
                raise ValueError("Only ExtractRenditionsElementType enum List is accepted for elements_to_extract_renditions")
            return self

        def with_table_structure_format(self, table_structure: TableStructureType):
            """
            adds the table structure format (currently csv only) for extracting structured information.

            :param table_structure: TableStructureType to be extracted
            :type table_structure: TableStructureType
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            :raises ValueError: if table_structure is None.
            """
            if table_structure and table_structure in TableStructureType:
                self._table_output_format = table_structure
            else:
                raise ValueError("Only TableStructureType enum is accepted for table_structure_format")
            return self

        def with_get_char_info(self, get_char_info: bool):
            """
            sets the Boolean specifying whether to add character level bounding boxes to output json

            :param get_char_info: Set True to extract character level bounding boxes information
            :type get_char_info: bool
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            """
            self._get_char_info = get_char_info
            return self

        def with_include_styling_info(self, include_styling_info: bool):
            """
            sets the Boolean specifying whether to add PDF Elements Styling Info to output json

            :param include_styling_info: Set True to extract PDF Elements Styling Info
            :type include_styling_info: bool
            :return: This Builder instance to add any additional parameters.
            :rtype: ExtractPDFOptions.Builder
            """
            self._include_styling_info = include_styling_info
            return self

        def build(self):
            return ExtractPDFOptions(self._elements_to_extract, self._elements_to_extract_renditions,
                                     self._get_char_info,
                                     self._table_output_format, self._include_styling_info)
