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


class OCRSupportedType(Enum):
    """
    Supported OCR types for OCRJob
    """

    # Ensures that text is searchable and selectable. This option keeps the original image, deskews it as needed,
    # and places an invisible text layer over it.
    SEARCHABLE_IMAGE = "searchable_image"

    # Ensures that text is searchable and selectable. This option keeps the original image and places an invisible
    # text layer over it. Recommended for cases requiring maximum fidelity to the original image.
    SEARCHABLE_IMAGE_EXACT = "searchable_image_exact"

    def __init__(self, ocr_type):
        """
        Constructs OCR Type from its string representation.

        :param ocr_type: String representation
        """
        self.type = ocr_type

    def get_type(self):
        """
        Returns the string representation of this OCRSupportedType.

        :return: String representation of this OCRSupportedType
        """
        return self.type
