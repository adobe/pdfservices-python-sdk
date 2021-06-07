# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.client_config import ClientConfig


class ExecutionContext:
    """
    Represents the execution context of an Operation.
    An execution context typically consists of the desired authentication credentials and client configurations such as timeouts.

    For each set of credentials, a ExecutionContext instance can be reused across operations.

    Sample Usage:

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
                .build()
            extract_pdf_operation.set_options(extract_pdf_options)

            result: FileRef = extract_pdf_operation.execute(execution_context)

            result.save_as(base_path + "/output/ExtractTextTableWithFigureTableRendition.zip")
        except (ServiceApiException, ServiceUsageException, SdkException):
            logging.exception("Exception encountered while executing operation")

    """

    @staticmethod
    def create(credentials: Credentials, client_config: ClientConfig = None):
        """Creates a context instance using the provided Credentials and ClientConfig

        :param credentials: A Credentials instance
        :type credentials: Credentials
        :param client_config: A ClientConfig instance for providing custom http timeouts, defaults to None
        :type client_config: ClientConfig, optional
        :return: A new :class:`ExecutionContext` instance
        :rtype: ExecutionContext
        """
        from adobe.pdfservices.operation.internal.internal_execution_context import InternalExecutionContext
        return InternalExecutionContext(credentials, client_config)
