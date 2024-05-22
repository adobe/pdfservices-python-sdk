# Copyright 2024 Adobe
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.

from typing import List, Optional

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.table_structure_type import TableStructureType
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class ExtractPDFParams(PDFServicesJobParams):
    """
    Parameters to extract content from PDF using
    :class:`ExtractPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job.ExtractPDFJob>`.
    """

    @enforce_types
    def __init__(self, *,
                 table_structure_type: TableStructureType = TableStructureType.XLSX,
                 add_char_info: bool = False,
                 styling_info: bool = False,
                 elements_to_extract: Optional[List] = None,
                 elements_to_extract_renditions: Optional[List] = None):
        """
        Construct a new :class:`.ExtractPDFParams`

        :param table_structure_type: TableStructureType for output type of table structure. (Optional, use key-value)
        :type table_structure_type: TableStructureType
        :param add_char_info: Boolean specifying whether to add character level bounding boxes to output json.
            (Optional, use key-value)
        :type add_char_info: bool
        :param styling_info: Boolean specifying whether to add styling information to output json.
            (Optional, use key-value)
        :type styling_info: bool
        :param elements_to_extract: List of :class:`ExtractElementType<adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_element_type.ExtractElementType>` to be extracted.
            (Optional, use key-value)
        :type elements_to_extract: List
        :param elements_to_extract_renditions: List of :class:`ExtractElementType<adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_renditions_element_type.ExtractRenditionsElementType>`.
            (Optional, use key-value)
        :type elements_to_extract_renditions: List
        """
        self.table_structure_type = table_structure_type
        self.add_char_info = add_char_info
        self.styling_info = styling_info
        self.elements_to_extract_renditions = elements_to_extract_renditions
        self.elements_to_extract = elements_to_extract

    def get_table_structure_type(self):
        """
        :return: Returns the TableStructureType of the resulting rendition
        :rtype: TableStructureType
        """
        return self.table_structure_type

    def get_add_char_info(self):
        """
        :return: Whether character level information was invoked for operation.
        :rtype: bool
        """
        return self.add_char_info

    def get_styling_info(self):
        """
        :return: Whether styling information was invoked for operation.
        :rtype: bool
        """
        return self.styling_info

    def get_elements_to_extract_renditions(self):
        """
        :return: Returns the list of :class:`ExtractElementType<adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_renditions_element_type.ExtractRenditionsElementType>` invoked for job.
        :rtype: list
        """
        return [element.__str__() for element in self.elements_to_extract_renditions] \
            if self.elements_to_extract_renditions is not None else None

    def get_elements_to_extract(self):
        """
        :return: The list of elements (Text and/or Tables) invoked for operation
        :rtype: list
        """
        return [element.__str__() for element in self.elements_to_extract] \
            if self.elements_to_extract is not None else None
