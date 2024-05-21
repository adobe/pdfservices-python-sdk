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
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges


class CombinePDFJobInput:
    json_hint = {
        'asset_id': 'assetID',
        'page_ranges': 'pageRanges',
        'external_asset': 'input'
    }

    def __init__(self, asset: Asset, page_ranges: PageRanges):
        self.__asset: Asset = asset
        self.__page_ranges = page_ranges
        if isinstance(asset, CloudAsset):
            self.asset_id = asset.get_asset_id()
        else:
            self.external_asset = asset

        if page_ranges is not None:
            self.page_ranges = page_ranges.get_ranges()

    def get_asset(self):
        return self.__asset

    def get_page_ranges(self):
        return self.__page_ranges

    def to_json(self):
        rand = json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
        print(rand)
        return rand
