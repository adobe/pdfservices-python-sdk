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


class AppearanceItem(Enum):
    """
    Supported elements to represent electronic seal required for
    :class:`AppearanceOptions<adobe.pdfservices.operation.pdfjobs.params.eseal.appearance_options.AppearanceOptions>`.
    """

    NAME = 'NAME'
    """
    Represents the name of the certificate owner.
    """

    DATE = 'DATE'
    """
    Represents the date of applying the electronic seal.
    """

    DISTINGUISHED_NAME = 'DISTINGUISHED_NAME'
    """
    Represents the distinguished name information of the certificate.
    """

    LABELS = 'LABELS'
    """
    Represents labels for seal information.
    """

    SEAL_IMAGE = 'SEAL_IMAGE'
    """
    Represents the background image to be used for sealing.
    """


    def __init__(self, appearance_item: str):
        self.appearance_item = appearance_item

    def get_appearance_item(self) -> str:
        return self.appearance_item
