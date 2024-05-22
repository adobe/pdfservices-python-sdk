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

from typing import Any

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.fragments import Fragments
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.output_format import OutputFormat
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class DocumentMergeParams(PDFServicesJobParams):
    """
    Parameters for document generation using
    :class:`DocumentMergeJob<adobe.pdfservices.operation.pdfjobs.jobs.document_merge_job.DocumentMergeJob>`
    """

    @enforce_types
    def __init__(self, json_data_for_merge: Any, *,
                 output_format: OutputFormat = OutputFormat.PDF,
                 fragments: Fragments = None):
        """
        Constructs a new :samp:`DocumentMergeParams` instance

        :param json_data_for_merge: json to be used in the document merge job; can not be None.
        :type json_data_for_merge: Any
        :param output_format: output format for the document merge result; (Optional, use key-value)
        :type output_format: OutputFormat
        :param fragments: fragments for document merge job; (Optional, use key-value)
        :type fragments: Fragments
        :return: DocumentMergeParams
        """
        self.__json_data_for_merge = json_data_for_merge
        self.__output_format = output_format
        self.__fragments = fragments

    def get_json_data_for_merge(self):
        """
        :return: JSON data for the document merge process
        """
        return self.__json_data_for_merge

    def get_output_format(self):
        """
        :return: output format for the document merge result
        """
        return self.__output_format

    def get_fragments(self):
        """
        :return: fragments for document merge job
        """
        return self.__fragments
