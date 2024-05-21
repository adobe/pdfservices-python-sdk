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
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.rotate_pages.angle import Angle


class RotatePageAction(PageAction):
    json_hint = {
        'page_ranges': 'pageRanges',
        'rotation_angle': 'angle',
    }

    def __init__(self, page_ranges: PageRanges, rotation_angle: Angle):
        super().__init__(page_ranges)
        self.rotation_angle = rotation_angle.value
        self.page_ranges = page_ranges.get_ranges()

    def get_rotation_angle(self):
        return self.rotation_angle
