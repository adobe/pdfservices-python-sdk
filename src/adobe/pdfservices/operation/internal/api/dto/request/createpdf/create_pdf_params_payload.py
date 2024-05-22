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

from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.pdfjobs.params.create_pdf.CreatePDFParams import CreatePDFParams


class CreatePDFParamsPayload:
    json_hint = {
        'document_language': 'documentLanguage',
        'create_tagged_pdf': 'createTaggedPDF'
    }

    def __init__(self, create_pdf_params: CreatePDFParams):
        self.create_tagged_pdf = False
        if create_pdf_params is not None:
            if create_pdf_params.get_document_language() is not None:
                self.document_language = create_pdf_params.get_document_language().get_document_language()
            if create_pdf_params.get_create_tagged_pdf() is not None:
                self.create_tagged_pdf = create_pdf_params.get_create_tagged_pdf()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
