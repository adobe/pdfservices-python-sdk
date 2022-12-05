# Copyright 2022 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

class AssetUploadURIResponse:
    json_hint = {
        'uploadUri': 'uploadUri',
        'assetID': 'assetID'
    }

    def __init__(self, upload_uri: str,
                 asset_id: str):
        super().__init__()
        self._upload_uri = upload_uri
        self._asset_iD = asset_id

    @property
    def upload_uri(self):
        return self._upload_uri

    @property
    def asset_id(self):
        return self._asset_id
