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


class AssetUploadURIRequest:
    json_hint = {
        'mediaType': 'mediaType'
    }

    def __init__(self, media_type: str):
        super().__init__()
        self.mediaType = media_type

    @property
    def media_type(self):
        return self.mediaType

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
