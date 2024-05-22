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


class PDFServicesMediaType(str, enum.Enum):


    AI = "application/illustrator"
    """Represents ai mime type."""

    BMP = "image/bmp"
    """Represents bmp mime type."""

    DOC = "application/msword"
    """Represents msword mime type."""

    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    """Represents docx mime type."""

    GIF = "image/gif"
    """Represents gif mime type."""

    HTML = "text/html"
    """Represents html mime type."""

    INDD = "application/x-indesign"
    """Represents indd mime type."""

    JPEG = "image/jpeg"
    """Represents jpeg mime type."""

    JPG = "image/jpeg"
    """Represents jpg mime type."""

    PDF = "application/pdf"
    """Represents pdf mime type."""

    PNG = "image/png"
    """Represents png mime type."""

    PPT = "application/vnd.ms-powerpoint"
    """Represents ppt mime type."""

    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    """Represents pptx mime type."""

    PSD = "image/vnd.adobe.photoshop"
    """Represents psd mime type."""

    RTF = "text/rtf"
    """Represents rtf mime type."""

    TIF = "image/tiff"
    """Represents tif mime type."""

    TIFF = "image/tiff"
    """Represents tiff mime type."""

    TXT = "text/plain"
    """Represents txt mime type."""

    XLS = "application/vnd.ms-excel"
    """Represents xls mime type."""

    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    """Represents xlsx mime type."""

    ZIP = "application/zip"
    """Represents zip mime type."""

    JSON = "application/json"
    """Represents json mime type."""

    CSV = "text/csv"
    """Represents csv mime type."""

    SVG = "image/svg+xml"
    """Represents svg mime type."""

    @property
    def mime_type(self):
        """
        :return: Media type of PDFServicesMediaType.
        """
        return self.value

    @property
    def extension(self):
        """
        :return: Extension of PDFServicesMediaType.
        """
        return self.name.lower()

    @staticmethod
    def get_from_extension(extension: str):
        """
        :return: PDFServicesMediaType for the given extension.
        """
        for extension_media_type_mapping in PDFServicesMediaType:
            if ('.' + extension_media_type_mapping.extension) == extension:
                return extension_media_type_mapping
        return None
