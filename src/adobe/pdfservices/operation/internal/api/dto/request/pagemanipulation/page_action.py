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

from abc import ABC

from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges


class PageAction(ABC):

    def __init__(self, page_ranges: PageRanges):
        self.__page_ranges = page_ranges

    def get_page_ranges(self):
        return self.__page_ranges
