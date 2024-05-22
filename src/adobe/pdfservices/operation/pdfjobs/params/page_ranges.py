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

from adobe.pdfservices.operation.internal.params.page_range import PageRange
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class PageRanges:
    """
    Page ranges of a file, inclusive of start and end page index, where page index starts from 1.
    """
    json_hint = {
        'ranges': 'pageRanges'
    }

    __RANGES_MAX_LIMIT = 100

    def __init__(self):
        """
        Constructs a new :samp:`PageRanges` instance with no pages added.
        """
        self.ranges = []

    @enforce_types
    def add_single_page(self, page: int):
        """
        Adds a single page. Page index starts from 1.
        :param page: single page index
        :type page: int
        """
        self.ranges.append(PageRange(page, page))
        return self

    @enforce_types
    def add_range(self, start: int, end: int):
        """
        Adds a page range. Page indexes start from 1.
        :param start: start page index, inclusive
        :type start: int
        :param end: end page index, inclusive
        :type start: int
        """
        self.ranges.append(PageRange(start, end))
        return self

    @enforce_types
    def add_all_from(self, start: int):
        """
        Adds a page range from start page index to the last page. Page index starts from 1.
        :param start: start page index
        :type start: int
        """
        self.ranges.append(PageRange(start, None))
        return self

    def add_all(self):
        """
        Adds a page range representing all pages.
        """
        self.ranges.append(PageRange(1, None))
        return self

    def __str__(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        :return: String representation
        """
        return ",".join(map(lambda r: PageRange(*r).__str__(), self.ranges))

    def validate(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        if len(self.ranges) > self.__RANGES_MAX_LIMIT:
            raise ValueError("Maximum allowed limit exceeded for page ranges.")

        for page_range in self.ranges:
            page_range.validate()

    def is_empty(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        return not self.ranges

    def get_ranges(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        return self.ranges

    def to_json(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
