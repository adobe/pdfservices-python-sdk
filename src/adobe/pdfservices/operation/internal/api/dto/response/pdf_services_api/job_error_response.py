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

class JobErrorResponse:

    def __init__(self, error_response: {}):
        error_content = error_response.get('error', None)
        if error_content is not None:
            self.code = error_content.get('code', None)
            self.message = error_content.get('message', None)
            self.status = error_content.get('status', None)

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_status(self):
        return self.status
