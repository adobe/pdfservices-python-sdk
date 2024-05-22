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


class FieldLocation:
    """
    Parameters specifying options related to seal field location coordinates required for
    :class:`FieldOptions<adobe.pdfservices.operation.pdfjobs.params.eseal.field_options.FieldOptions>`
    """

    @enforce_types
    def __init__(self, left: int, top: int, right: int, bottom: int):
        """
        :param left: the left coordinate of field location
        :type left: int
        :param top: the top coordinate of field location
        :type top: int
        :param right: the right coordinate of field location
        :type right: int
        :param bottom: the bottom coordinate of field location
        :type bottom: int
        """
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    # getters for left, top, right, bottom
    def get_left(self):
        """
        :return: the left coordinate of field location
        :rtype: int
        """
        return self._left

    def get_top(self):
        """
        :return: the top coordinate of field location
        :rtype: int
        """
        return self._top

    def get_right(self):
        """
        :return: the right coordinate of field location
        :rtype: int
        """
        return self._right

    def get_bottom(self):
        """
        :return: the bottom coordinate of field location
        :rtype: int
        """
        return self._bottom

    def to_dict(self):
        return {
            'top': self._top,
            'left': self._left,
            'right': self._right,
            'bottom': self._bottom,
        }
