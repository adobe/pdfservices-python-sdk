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

import enum


class Region(str, enum.Enum):
    """
    Supported regions to be used with :class:`ClientConfig<adobe.pdfservices.operation.config.client_config.ClientConfig>`.
    """

    US = "us"
    """
    Represents
    "US"
    region
    """

    EU = "eu"
    """
    Represents
    "Europe"
    region
    """
