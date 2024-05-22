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


from adobe.pdfservices.operation.io.asset import Asset


class CloudAsset(Asset):
    """
    This class represents an asset stored in Adobe internal storage.
    """

    def __init__(self, asset_id, download_uri=None):
        """
        Constructs an instance of :samp:`CloudAsset`.

        :param asset_id: assetId of the asset.
        :type asset_id: str
        :param download_uri: downloadURI of the asset.
        :type download_uri: str
        """
        self.asset_id = asset_id
        self.download_uri = download_uri

    def get_asset_id(self):
        """
        :return: the assetId of the asset.
        :rtype: str
        """
        return self.asset_id

    def get_download_uri(self):
        """
        :return: the downloadURI of the asset.
        :rtype: str
        """
        return self.download_uri
