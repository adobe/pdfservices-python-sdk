# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import io
import logging
import os
from io import BufferedWriter

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.service_constants import ServiceConstants
from adobe.pdfservices.operation.internal.extension_media_type_mapping import ExtensionMediaTypeMapping
from adobe.pdfservices.operation.internal.util.path_util import get_extension
from adobe.pdfservices.operation.io.file_ref import FileRef


class FileRefImpl(FileRef):

    def get_media_type(self):
        return self._media_type

    def get_as_stream(self):
        if self._file_path:
            return open(self._file_path, 'rb')
        else:
            file_stream = self._input_stream
        return file_stream

    def save_as(self, destination_file_path):
        if self._is_operation_result():
            self._logger.info(
                "Moving file at {tmp_file_path} to target {target_path}".format(tmp_file_path=self._file_path,
                                                                                target_path=destination_file_path))
            abs_path = os.path.abspath(destination_file_path)
            dir = os.path.dirname(abs_path)
            if not os.path.exists(dir):
                os.mkdir(dir)
            if not os.path.exists(abs_path):
                os.rename(self._file_path, abs_path)
                return
            raise SdkException("Output file {file} exists".format(file=destination_file_path))
        else:
            self._logger.error(
                "Invalid use of save_as(). Method invoked on FileRef instance which does not point to an operation "
                "result")
            raise AttributeError("Method save_as only allowed on operation results")

    def write_to_stream(self, writer_stream: BufferedWriter):
        if self._is_operation_result():
            with open(self._file_path, "rb", -1) as file:
                while True:
                    buffer = file.read(io.DEFAULT_BUFFER_SIZE)
                    writer_stream.write(buffer)
                    if len(buffer) < io.DEFAULT_BUFFER_SIZE:
                        break
            writer_stream.close()
            self._logger.info("Writing file at {tmp_file_path} to writer stream".format(tmp_file_path=self._file_path))
        else:
            self._logger.error(
                "Invalid use of write_to_stream(). Method invoked on FileRef instance which does not point to an operation "
                "result")
            raise AttributeError("Method write_to_stream() only allowed on operation results")

    def _is_operation_result(self):
        return self._file_path and ServiceConstants.OPERATION_RESULT_TEMP_DIRECTORY in self._file_path

    def __init__(self, file_path=None, input_stream=None, media_type=None):
        if file_path:
            self._file_path = file_path
            if not media_type:
                extension = get_extension(file_path)
                extension_media_type_mapping = ExtensionMediaTypeMapping.get_from_extension(extension)
                media_type = extension_media_type_mapping.mime_type if extension_media_type_mapping else None
            self._media_type = media_type
            self._input_stream = None
        elif input_stream:
            self._input_stream = input_stream
            self._media_type = media_type
            self._file_path = None
        else:
            raise ValueError("One of file path or input stream sources are mandatory")
        self._logger = logging.getLogger(__name__)

