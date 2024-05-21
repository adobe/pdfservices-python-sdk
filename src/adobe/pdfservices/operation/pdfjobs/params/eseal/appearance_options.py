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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.eseal.appearance_item import AppearanceItem


class AppearanceOptions:
    """
    Parameters specifying set of elements (i.e. appearance items) to represent electronic seal required for
    :class:`PDFElectronicSealParams<adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params.PDFElectronicSealParams>`.
    """

    def __init__(self):
        self._appearance_options = []

    @enforce_types
    def add_item(self, appearance_option: AppearanceItem):
        """
        :param appearance_option: AppearanceItem to be added to AppearanceOptions, can not be None.
        :type appearance_option: AppearanceItem
        """
        self._appearance_options.append(appearance_option.get_appearance_item())
        return self

    def get_appearance_options(self):
        """
        :return: List of Appearance Items
        """
        return self._appearance_options
