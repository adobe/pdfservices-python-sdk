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

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action import PageAction


class PageActions:

    def __init__(self):
        self._actions = []

    def add_action(self, action: PageAction):
        self._actions.append(action)

    def get_actions(self):
        return self._actions

    def is_empty(self):
        if len(self._actions) == 0:
            return True
        return False

    def get_length(self):
        return len(self._actions)
