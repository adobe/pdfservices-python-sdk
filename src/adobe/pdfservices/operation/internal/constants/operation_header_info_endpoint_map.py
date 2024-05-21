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


class OperationHeaderInfoEndpointMap(Enum):
    CREATE_PDF = ("Create PDF Operation", "createpdf")
    COMBINE_PDF = ("Combine Files Operation", "combinepdf")
    EXPORT_PDF = ("Export PDF Operation", "exportpdf")
    EXPORT_PDF_TO_IMAGES = ("Export PDF to Images Operation", "pdftoimages")
    HTML_TO_PDF = ("HTML to PDF Operation", "htmltopdf")
    OCR = ("OCR Operation", "ocr")
    COMPRESS_PDF = ("Compress PDF Operation", "compresspdf")
    LINEARIZE_PDF = ("Linearize PDF Operation", "linearizepdf")
    PROTECT_PDF = ("Protect PDF Operation", "protectpdf")
    INSERT_PAGES = ("Insert Pages Operation", "combinepdf")
    REPLACE_PAGES = ("Replace Pages Operation", "combinepdf")
    REORDER_PAGES = ("Reorder Pages Operation", "combinepdf")
    ROTATE_PAGES = ("Reorder Pages Operation", "pagemanipulation")
    DELETE_PAGES = ("Delete Pages Operation", "pagemanipulation")
    REMOVE_PROTECTION = ("Remove Protection Operation", "removeprotection")
    SPLIT_PDF = ("Split PDF Operation", "splitpdf")
    MERGE_DOCUMENT = ("Document Merge Operation", "documentgeneration")
    EXTRACT_PDF = ("Extract PDF Operation", "extractpdf")
    PDF_PROPERTIES = ("PDF Properties Operation", "pdfproperties")
    AUTO_TAG = ("PDF Autotag Operation", "autotag")
    E_SEAL = ("Electronic Seal Operation", "electronicseal")

    def __init__(self, header_info, endpoint):
        self.header_info = header_info
        self.endpoint = endpoint

    def get_header_info(self):
        return self.header_info

    def get_endpoint(self):
        return self.endpoint
