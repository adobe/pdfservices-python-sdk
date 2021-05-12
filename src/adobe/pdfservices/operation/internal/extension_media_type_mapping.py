# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import enum


class ExtensionMediaTypeMapping(str, enum.Enum):
    PDF = "application/pdf"
    ZIP = "application/zip"

    @property
    def mime_type(self):
        return self.value

    @property
    def extension(self):
        return self.name.lower()

    @staticmethod
    def get_from_extension(extension: str):
        for extension_media_type_mapping in ExtensionMediaTypeMapping:
            if ('.' + extension_media_type_mapping.extension) == extension:
                return extension_media_type_mapping
        return None
