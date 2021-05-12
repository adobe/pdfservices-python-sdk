# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Optional


class FileRef(ABC):
    """
    This class represents a local file. It is typically used by an SDK Operation which accepts or returns files.

    When a FileRef instance is created by this SDK while referring to a temporary file location, calling any of the
    methods to save the fileRef (For example, :func:`~create_from_stream` etc.) will delete the temporary file.
    """

    @staticmethod
    def create_from_local_file(local_source: str, media_type: Optional[str] = None):
        """
        Creates a FileRef instance from a local file path. If no media type is provided, it will be inferred
        from the file extension.

        :param local_source: Local file path, either absolute path or relative to the working directory.
        :type local_source: str
        :param media_type: Media type to identify the local file format, defaults to None
        :type media_type: str, optional, defaults to None
        :return: A FileRef instance.
        :rtype: FileRef
        """
        from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
        if not local_source:
            raise ValueError("Source file path must not be null")
        return FileRefImpl(file_path=local_source, media_type=media_type)

    @staticmethod
    def create_from_stream(input_stream: BufferedReader, media_type: str):
        """
        Creates a FileRef instance from a readable stream using the specified media type.
        The stream is not read by this method but by consumers of file content i.e. the execute method of an operation
        such as :func:`~ExtractionPDFOperation.execute`.

        :param input_stream: Readable Stream representing the file.
        :type input_stream: BufferedReader
        :param media_type: Media type to identify the file format.
        :type media_type: str
        :return: A FileRef instance.
        :rtype: FileRef
        """
        from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
        if not input_stream:
            raise ValueError("Source input stream must not be null")
        if not media_type:
            raise ValueError("Source file media_type must not be null")
        return FileRefImpl(input_stream=input_stream, media_type=media_type)

    @abstractmethod
    def save_as(self, local_file_path: str):
        pass

    @abstractmethod
    def write_to_stream(self, writer_stream):
        pass