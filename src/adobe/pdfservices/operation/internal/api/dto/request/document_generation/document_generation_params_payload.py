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
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.document_merge_params import DocumentMergeParams


class DocumentGenerationParamsPayload:
    json_hint = {
        'output_format': 'outputFormat',
        'json_data_for_merge': 'jsonDataForMerge',
        'fragments': 'fragments'
    }

    def __init__(self, document_merge_params: DocumentMergeParams):
        if document_merge_params.get_fragments() is not None:
            self.fragments = document_merge_params.get_fragments().get_fragments_list()
        self.json_data_for_merge = document_merge_params.get_json_data_for_merge()
        self.output_format = document_merge_params.get_output_format().get_format()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
