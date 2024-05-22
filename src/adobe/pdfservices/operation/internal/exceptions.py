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


class OperationException(Exception):

    def __init__(self, message, error_message, request_tracking_id, status_code,
                 error_code=None, report_error_code=None):
        self.message = message
        self.error_message = error_message
        self.request_tracking_id = request_tracking_id
        self.status_code = status_code
        self._error_code = error_code
        self._report_error_code = report_error_code

    @property
    def error_code(self):
        return self._report_error_code if self._report_error_code else self._error_code
