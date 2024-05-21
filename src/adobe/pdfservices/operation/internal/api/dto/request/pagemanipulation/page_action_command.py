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

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.delete_page_action import \
    DeletePageAction
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action import PageAction
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.rotate_page_action import \
    RotatePageAction
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class PageActionCommand:
    json_hint = {
        'delete_action': 'delete',
        'rotate_action': 'rotate'
    }

    def __init__(self, *, delete_action: DeletePageAction = None, rotate_action: RotatePageAction = None):
        self.delete_action = delete_action
        self.rotate_action = rotate_action

    @staticmethod
    def create_from(action: PageAction):
        if isinstance(action, DeletePageAction):
            page_action_command = PageActionCommand(delete_action=action)
        elif isinstance(action, RotatePageAction):
            page_action_command = PageActionCommand(rotate_action=action)

        return page_action_command

    def to_json(self):
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
