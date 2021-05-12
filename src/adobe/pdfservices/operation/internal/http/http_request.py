# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod


class HttpRequest:

    # (url, data/files, headers, authenticator (if none its not authenticated), socket_timeout, connect_timeout)
    def __init__(self, http_method: HttpMethod, url: str, headers: dict, data=None, files=None,
                 authenticator: Authenticator = None, read_timeout=None, connect_timeout=None, retryable:bool=False):
        self.method = http_method
        self.url = url
        self.headers = headers
        self.data = data
        self.files = files
        self.authenticator = authenticator
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout
        self.retryable = retryable
