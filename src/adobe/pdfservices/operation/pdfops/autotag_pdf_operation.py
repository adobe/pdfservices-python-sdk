# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging

from adobe.pdfservices.operation.exception.exceptions import ServiceApiException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_output_files import \
    AutotagPDFOutputFiles
from adobe.pdfservices.operation.internal.exceptions import OperationException
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
from adobe.pdfservices.operation.internal.service.autotagpdf.autotag_pdf_api import AutotagPDFAPI
from adobe.pdfservices.operation.internal.util.file_utils import get_transaction_id
from adobe.pdfservices.operation.internal.util.path_util import get_temporary_destination_path
from adobe.pdfservices.operation.internal.util.validation_util import validate_media_type
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.operation import Operation
from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions


class AutotagPDFOperation(Operation):
    """ An operation that enables clients to improve accessibility of the PDF document. It generates the tagged PDF,
    along with an optional XLSX report providing detailed information about the added tags. The operation replaces any
    existing tags within the input document, so it provides the most benefit for PDFs that have no tags or low-quality
    tags.

    Sample usage.

    .. code-block:: python

        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            credentials = Credentials.service_account_credentials_builder() \\
                .from_file(base_path + "/pdfservices-api-credentials.json") \\
                .build()

            execution_context = ExecutionContext.create(credentials)
            autotag_pdf_operation = AutotagPDFOperation.create_new()

            input_file_path = 'autotagPdfInput.pdf'
            source = FileRef.create_from_local_file(base_path + "/resources/" + input_file_path)
            autotag_pdf_operation.set_input(source)

            autotag_pdf_options: AutotagPDFOptions = AutotagPDFOptions.builder() \\
                .with_shift_headings() \\
                .with_generate_report() \\
                .build()
            autotag_pdf_operation.set_options(autotag_pdf_options)

            autotag_output_files: AutotagPDFOutputFiles = autotag_pdf_operation.execute(execution_context)

            input_file_name = Path(input_file_path).stem
            base_output_path = base_path + "/output/AutotagPDFWithOptions/"

            Path(base_output_path).mkdir(parents=True, exist_ok=True)
            tagged_pdf_path = f'{base_output_path}{input_file_name}-tagged.pdf'
            report_path = f'{base_output_path}{input_file_name}-report.xlsx'

            autotag_output_files.save_pdf_file(tagged_pdf_path)
            autotag_output_files.save_xls_file(report_path)

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    """

    SUPPORTED_SOURCE_MEDIA_TYPES = {ExtensionMediaTypeMapping.PDF.mime_type}
    """ Supported source file formats for :class:`AutotagPdfOperation` is .pdf."""

    __create_key = object()

    def __init__(self, create_key):
        assert (create_key == AutotagPDFOperation.__create_key), \
            "Operation objects must be created using create_new"
        self._source_file_ref = None
        self._is_invoked = False
        self._autotag_pdf_options = None
        self._logger = logging.getLogger(__name__)

    @classmethod
    def create_new(cls):
        """ creates a new instance of `AutotagPDFOperation`.

        :return: A new instance of AutotagPDFOperation
        :rtype: AutotagPDFOperation
        """
        return AutotagPDFOperation(cls.__create_key)

    def set_options(self, autotag_pdf_options: AutotagPDFOptions):
        """ sets the AutotagPDFOptions.

        :param autotag_pdf_options: AutotagPDFOptions to set.
        :type autotag_pdf_options: AutotagPDFOptions
        :return: This instance to add any additional parameters.
        :rtype: AutotagPDFOperation
        """
        if not isinstance(autotag_pdf_options, AutotagPDFOptions):
            raise ValueError("Only AutotagPDFOptions type instance is accepted")
        self._autotag_pdf_options = autotag_pdf_options
        return self

    def set_input(self, source_file_ref: FileRef):
        """
        Sets an input file.

        :param source_file_ref: An input file.
        :type source_file_ref: FileRef
        :return: This instance to add any additional parameters.
        :rtype: AutotagPDFOperation
        """
        if not isinstance(source_file_ref, FileRef):
            raise ValueError("Invalid input file type. Only FileRef type instance is accepted")
        self._source_file_ref = source_file_ref
        return self

    def execute(self, execution_context: ExecutionContext):
        """
        Executes this operation synchronously using the supplied context and returns a new AutotagPDFOutputFiles
        instance for the generated tagged pdf file and XLSX report file. The resulting file may be stored in the system
        temporary directory.
        See :class:`adobe.pdfservices.operation.io.file_ref.FileRef` for how temporary resources are cleaned up.

        :param execution_context: The context in which the operation will be executed.
        :type execution_context: ExecutionContext
        :return: The instance of AutotagPDFOutputFiles.
        :rtype: AutotagPDFOutputFiles
        :raises ServiceApiException: if an API call results in an error response.
        """
        try:
            self._validate(execution_context=execution_context)
            self._logger.info("All validations successfully done. Beginning AutotagPDF operation execution")

            location = AutotagPDFAPI.autotag_pdf(execution_context, self._source_file_ref, self._autotag_pdf_options)
            self._is_invoked = True
            file_location_pdf = get_temporary_destination_path(target_extension=ExtensionMediaTypeMapping.PDF.extension)
            file_location_xlsx = get_temporary_destination_path(
                target_extension=ExtensionMediaTypeMapping.XLSX.extension)
            autotag_pdf_output_files: AutotagPDFOutputFiles = AutotagPDFAPI.download_and_save(location=location,
                                                                                              context=execution_context,
                                                                                              file_location_pdf=file_location_pdf,
                                                                                              file_location_xlsx=file_location_xlsx)
            self._logger.info("Autotag Operation Successful - Transaction ID: %s", get_transaction_id(location))
            return autotag_pdf_output_files
        except OperationException as oex:
            raise ServiceApiException(message=oex.error_message, error_code=oex.error_code,
                                      request_tracking_id=oex.request_tracking_id,
                                      status_code=oex.status_code) from None

    def _validate_invocation_count(self):
        if self._is_invoked:
            raise ValueError("Operation instance must not be reused, can only be invoked once")

    def _validate(self, execution_context: InternalExecutionContext):
        self._validate_invocation_count()
        if not execution_context:
            raise ValueError("Client Context not initialized before invoking the operation")
        execution_context.validate()
        if not self._source_file_ref:
            raise ValueError("No input was set for operation")
        validate_media_type(self.SUPPORTED_SOURCE_MEDIA_TYPES, self._source_file_ref.get_media_type())
