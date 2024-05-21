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

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action_commands import \
    PageActionCommands
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class PageManipulationParamsPayload:
    json_hint = {
        'page_actions': 'pageActions'
    }

    def __init__(self, page_action_commands: PageActionCommands):
        self.page_actions = page_action_commands.get_commands()

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
