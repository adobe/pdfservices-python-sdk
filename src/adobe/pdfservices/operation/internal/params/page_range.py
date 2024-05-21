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

import json

from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class PageRange:
    json_hint = {
        'start': 'start',
        'end': 'end'
    }

    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def validate(self):
        if (self.end is not None and self.start > self.end) or self.start <= 0:
            raise ValueError("Invalid page range specified")

    def __str__(self):
        if self.end is not None and self.start == self.end:
            return str(self.start)
        else:
            if self.end is None:
                return str(self.start) + "-"
            else:
                return str(self.start) + "-" + str(self.end)

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
