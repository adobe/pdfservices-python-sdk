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
from adobe.pdfservices.operation.internal.util.path_util import get_file_path


def read_conf_file_content(file_path):
    with open(get_file_path(file_path)) as file:
        return file.read()


def read_file_content(file_path):
    with open(get_file_path(file_path), "rb") as file:
        return file.read()


def get_transaction_id(location_url: str):
    if not location_url:
        return 'UnknownRequestID'
    return location_url.split("/")[-1]
