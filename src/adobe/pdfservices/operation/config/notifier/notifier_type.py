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


class NotifierType(Enum):
    """
    Notifier Type Mapping.
    """

    CALLBACK = "CALLBACK"
    """
    Callback notifier type.
    """

    def __str__(self):
        """
        :return: string representation of :class:`.NotifierType`.
        :rtype: str
        """
        return self.value
