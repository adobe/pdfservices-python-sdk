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

from enum import Enum


class ExternalStorageType(Enum):
    """
    Represents external storage types.
    """

    SHAREPOINT = "SHAREPOINT"
    """
    Represents Sharepoint storage.
    """

    S3 = "S3"
    """
    Represents S3 storage.
    """

    DROPBOX = "DROPBOX"
    """
    Represents Dropbox storage.
    """

    BLOB = "BLOB"
    """
    Represents Blob storage.
    """

    def __init__(self, storage_type):
        self.storage_type = storage_type

    @classmethod
    def get(cls, storage_type: str):
        """
        Returns ExternalStorageType instance for its string representation.

        :param storage_type: Storage type code
        :type storage_type: str
        """
        if storage_type is not None:
            for ext_storage in cls:
                if ext_storage.storage_type == storage_type.upper():
                    return ext_storage
        raise ValueError("Invalid value for Storage Type.")

    def __str__(self):
        """
        Returns the string representation of the storage type.
        :return: Storage type
        """
        return self.storage_type
