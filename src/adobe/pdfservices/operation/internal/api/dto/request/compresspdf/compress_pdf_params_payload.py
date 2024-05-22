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
from adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compress_pdf_params import CompressPDFParams
from adobe.pdfservices.operation.pdfjobs.params.compress_pdf.compression_level import CompressionLevel


class CompressPDFParamsPayload:
    json_hint = {
        'compression_level': 'compressionLevel'
    }

    def __init__(self, compress_pdf_params: CompressPDFParams):
        self.compression_level = CompressionLevel.MEDIUM.get_compression_level()
        if compress_pdf_params is not None:
            self.compression_level = compress_pdf_params.get_compression_level().get_compression_level()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
