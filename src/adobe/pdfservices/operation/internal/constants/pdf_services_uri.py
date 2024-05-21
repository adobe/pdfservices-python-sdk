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

from adobe.pdfservices.operation.region import Region


class PDFServicesURI:
    URI = "https://pdf-services.adobe.io"
    US_URI = "https://pdf-services-ue1.adobe.io"
    EU_URI = "https://pdf-services-ew1.adobe.io"

    REGION_URI_MAP = {
        Region.US: US_URI,
        Region.EU: EU_URI
    }

    @staticmethod
    def get_uri_for_region(region: Region):
        return PDFServicesURI.REGION_URI_MAP.get(region, PDFServicesURI.get_default_uri()) if region is not None \
            else PDFServicesURI.URI

    @staticmethod
    def get_default_uri():
        return PDFServicesURI.URI
