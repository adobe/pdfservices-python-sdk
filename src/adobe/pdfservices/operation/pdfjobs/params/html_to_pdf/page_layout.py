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
import math

from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class PageLayout:
    """
    Represents a page layout with dimensions in inches.
    """

    DEFAULT_PAGE_HEIGHT = 11.0
    """
    Default value of the page height (in inches)
    """

    DEFAULT_PAGE_WIDTH = 8.5
    """
    Default value of the page width (in inches)
    """

    json_hint = {
        'page_height': 'pageHeight',
        'page_width': 'pageWidth'
    }

    def __init__(self, page_height: float = DEFAULT_PAGE_HEIGHT, page_width: float = DEFAULT_PAGE_WIDTH):
        """
        Constructor to initialize a default page layout.
        The default layout sets the height as 11 inches and width as 8.5 inches.

        :param page_height: Height of the page in inches, can not be None
        :type page_height: float
        :param page_width: Width of the page in inches
        :type page_width: float
        """
        if math.isinf(page_height) or math.isnan(page_height):
            raise SdkException(message="Invalid page height value")
        if math.isinf(page_width) or math.isnan(page_width):
            raise SdkException(message="Invalid page width value")

        self.page_height = page_height
        self.page_width = page_width

    def to_json(self):
        """
        :return: JSON representation of this class, used internally by sdk.
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
