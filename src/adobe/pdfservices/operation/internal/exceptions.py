# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

class OperationException(Exception):

    def __init__(self, message, error_message, request_tracking_id, status_code, error_code = None, report_error_code = None):
        self.message = message
        self.error_message = error_message
        self.request_tracking_id = request_tracking_id
        self.status_code = status_code
        self._error_code = error_code
        self._report_error_code = report_error_code

    @property
    def error_code(self):
        return self._report_error_code if self._report_error_code else self._error_code
