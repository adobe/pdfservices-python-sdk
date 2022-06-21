# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
import os
import tempfile
import uuid
from typing import Optional

from adobe.pdfservices.operation.internal.service_constants import ServiceConstants


def get_extension(file_path):
    filename, extension = os.path.splitext(file_path)
    return extension


def get_file_path(file_path):
    if not os.path.isabs(file_path):
        return os.path.join(os.getcwd(), file_path)
    return file_path


def conf_file_abs_path(file_path):
    return get_file_path(file_path)


def get_random_file_name(extension: str):
    if extension:
        if not extension.startswith("."):
            extension = "." + extension
        return uuid.uuid1().hex + extension
    return None


def get_base_name(file_path: str):
    if file_path:
        return os.path.basename(file_path).split(".")[0]
    return ""


def get_file_name_with_extension(base_name: str, target_extension: str):
    if not target_extension:
        return base_name
    if target_extension.startswith('.'):
        return base_name + target_extension
    return base_name + '.' + target_extension


def get_temporary_destination_path(target_extension: str, file_name: Optional[str] = None):
    if not file_name or file_name.isspace():
        destination_file_name = get_random_file_name(extension=target_extension)
    else:
        destination_file_name = get_file_name_with_extension(get_base_name(file_name), target_extension)
    return "{path_dir}{path_sep}{file_name}".format(path_dir=get_temporary_directory_path(),
                                                    path_sep=os.path.sep,
                                                    file_name=destination_file_name)


def get_temporary_directory_path():
    system_temp_dir = tempfile.gettempdir()
    if system_temp_dir.endswith(os.path.sep):
        temp_dir_path = "{temp_dir}{result_dir}".format(temp_dir=system_temp_dir,
                                                        result_dir=ServiceConstants.OPERATION_RESULT_TEMP_DIRECTORY)
    else:
        temp_dir_path = "{temp_dir}{path_sep}{result_dir}".format(temp_dir=system_temp_dir,
                                                                  path_sep=os.path.sep,
                                                                  result_dir=ServiceConstants.OPERATION_RESULT_TEMP_DIRECTORY)
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)
    return temp_dir_path
