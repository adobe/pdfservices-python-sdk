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

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_action_command import \
    PageActionCommand


class PageActionCommands:
    def __init__(self):
        self._page_action_commands = []

    def add_command(self, command: PageActionCommand):
        self._page_action_commands.append(command)

    def get_commands(self):
        return self._page_action_commands
