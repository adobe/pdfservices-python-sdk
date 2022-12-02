# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
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
