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

from typing import List


class Fragments:
    """
    Class for providing support for Fragments. To know more about fragments
    use-case in document generation and document templates, `Click Here <http://www.adobe.com/go/dcdocgen_fragments_support>`_.
    """

    def __init__(self):
        """
        Constructs a new :samp:`Fragments` instance
        """
        self.__fragment_list = []

    def add_fragment(self, fragment):
        """
        To add fragment dictionary into the fragments list.

        :param fragment: fragment dictionary to be added into the fragments list.
        """
        self.__fragment_list.append(fragment)

    def add_fragments(self, fragments: List):
        """
        To add List of fragment dictionaries into the fragments list.

        :param fragments: fragment dictionary list to be added into the fragments list.
        """
        self.__fragment_list.extend(fragments)

    def get_fragments_list(self):
        """
        :return: list of fragments.
        """
        return self.__fragment_list
