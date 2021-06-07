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

from adobe.pdfservices.operation.exception.exceptions import ServiceApiException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.api.cpf_api import CPFApi
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.service.extract_pdf_api import ExtractPDFAPI
from adobe.pdfservices.operation.internal.util.file_utils import get_transaction_id
from adobe.pdfservices.operation.internal.util.path_util import get_temporary_destination_path
from adobe.pdfservices.operation.internal.util.validation_util import validate_media_type
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.operation import Operation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions


class ExtractPDFOperation(Operation):
    """An Operation that extracts pdf elements such as text and tables in a structured format from a PDF, along
    with renditions for tables and figures.

    Sample usage.

    .. code-block:: python

        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            credentials = Credentials.service_account_credentials_builder() \\
                .from_file(base_path + "/pdfservices-api-credentials.json") \\
                .build()

            execution_context = ExecutionContext.create(credentials)
            extract_pdf_operation = ExtractPDFOperation.create_new()

            source = FileRef.create_from_local_file(base_path + "/resources/extractPdfInput.pdf")
            extract_pdf_operation.set_input(source)

            extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \\
                .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \\
                .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES, ExtractRenditionsElementType.FIGURES]) \\
                .with_get_char_info(True) \\
                .with_include_styling_info(True) \\
                .build()
            extract_pdf_operation.set_options(extract_pdf_options)

            result: FileRef = extract_pdf_operation.execute(execution_context)

            result.save_as(base_path + "/output/ExtractTextTableWithFigureTableRendition.zip")
        except (ServiceApiException, ServiceUsageException, SdkException):
            logging.exception("Exception encountered while executing operation")

    """

    SUPPORTED_SOURCE_MEDIA_TYPES = {ExtensionMediaTypeMapping.PDF.mime_type}
    """ Supported source file formats for :class:`ExtractPdfOperation` is .pdf."""

    __create_key = object()

    def __init__(self, create_key):
        assert (create_key == ExtractPDFOperation.__create_key), \
            "Operation objects must be created using create_new"
        self._source_file_ref = None
        self._is_invoked = False
        self._extract_pdf_options = None
        self._logger = logging.getLogger(__name__)

    @classmethod
    def create_new(cls):
        """ creates a new instance of `ExtractPDFOperation`.

        :return: A new instance of ExtractPDFOperation
        :rtype: ExtractPDFOperation
        """
        return ExtractPDFOperation(cls.__create_key)

    def set_options(self, extract_pdf_options: ExtractPDFOptions):
        """ sets the ExtractPDFOptions.

        :param extract_pdf_options: ExtractPDFOptions to set.
        :type extract_pdf_options: ExtractPDFOptions
        :return: This instance to add any additional parameters.
        :rtype: ExtractPDFOperation
        """
        if not isinstance(extract_pdf_options, ExtractPDFOptions):
            raise ValueError("Only ExtractPDFOptions type instance is accepted")
        self._extract_pdf_options = extract_pdf_options
        return self

    def set_input(self, source_file_ref: FileRef):
        """
        Sets an input file.

        :param source_file_ref: An input file.
        :type source_file_ref: FileRef
        :return: This instance to add any additional parameters.
        :rtype: ExtractPDFOperation
        """
        if not isinstance(source_file_ref, FileRef):
            raise ValueError("Only FileRef type instance is accepted")
        self._source_file_ref = source_file_ref
        return self

    def execute(self, execution_context: ExecutionContext):
        """
        Executes this operation synchronously using the supplied context and returns a new FileRef instance for the resulting Zip file.
        The resulting file may be stored in the system temporary directory. See :class:`adobe.pdfservices.operation.io.file_ref.FileRef` for how temporary resources are cleaned up.

        :param execution_context: The context in which the operation will be executed.
        :type execution_context: ExecutionContext
        :return: The FileRef to the result.
        :rtype: FileRef
        :raises ServiceApiException: if an API call results in an error response.
        """
        try:
            self._validate_invocation_count()
            self._validate(execution_context=execution_context)
            self._logger.info("All validations successfully done. Beginning ExtractPDF operation execution")

            location = ExtractPDFAPI.extract_pdf(execution_context, self._source_file_ref, self._extract_pdf_options)
            self._is_invoked = True
            file_location = get_temporary_destination_path(target_extension=ExtensionMediaTypeMapping.ZIP.extension)
            ExtractPDFAPI.download_and_save(location=location, context=execution_context, file_location=file_location)
            self._logger.info("Extract Operation Successful - Transaction ID: %s", get_transaction_id(location))
            return FileRef.create_from_local_file(file_location)
        except OperationException as oex:
            raise ServiceApiException(message=oex.error_message, error_code=oex.error_code,
                                      request_tracking_id=oex.request_tracking_id, status_code=oex.status_code)

    def _validate_invocation_count(self):
        if self._is_invoked:
            self._logger.error("Operation instance must only be invoked once")
            raise ValueError("Operation instance must not be reused, can only be invoked once")

    def _validate(self, execution_context:InternalExecutionContext):
        if not execution_context:
            raise ValueError("Client Context not initialized before invoking the operation")
        execution_context.validate()
        if not self._source_file_ref:
            raise ValueError("No input was set for operation")
        validate_media_type(self.SUPPORTED_SOURCE_MEDIA_TYPES, self._source_file_ref.get_media_type())