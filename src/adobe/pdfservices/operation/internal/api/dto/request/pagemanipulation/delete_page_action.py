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


class DeletePageAction(PageAction):
    json_hint = {
        'page_ranges': 'pageRanges',
    }

    def __init__(self, page_ranges):
        super().__init__(page_ranges)
        self.type = 'delete'
        self.page_ranges = page_ranges.get_ranges()

    def get_type(self):
        return self.type
