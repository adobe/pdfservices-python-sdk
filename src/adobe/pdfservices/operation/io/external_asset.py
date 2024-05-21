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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.io.external_storage_type import ExternalStorageType


class ExternalAsset(Asset):
    """
    This class represents an asset stored in an external storage.
    """

    json_hint = {
        'uri': 'uri',
        'external_storage_type': 'storage'
    }
    """
    For JSON Representation of this class, used internally by SDK.
    """

    @enforce_types
    def __init__(self, uri: str, *,
                 external_storage_type: ExternalStorageType = None):
        """
        Constructs an instance of :samp:`ExternalAsset`.

        :param uri: URI of the external asset, can not be None.
        :type uri: str
        :param external_storage_type: external storage type. (Optional, use key-value)
        :type external_storage_type: ExternalStorageType
        """
        self.uri = uri
        if external_storage_type is not None:
            self.external_storage_type = external_storage_type.__str__()

    def get_uri(self):
        """
        :return: the URI of the external asset.
        :rtype: str
        """
        return self.uri

    def get_external_storage_type(self):
        """
        :return: the externalStorageType of the external asset.
        :rtype: ExternalStorageType
        """
        return self.external_storage_type

    def to_json(self):
        """
        :return: representation of ExternalAsset as a JSON string, used internally by the SDK.
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
