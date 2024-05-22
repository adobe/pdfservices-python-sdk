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

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.permission import Permission


class Permissions:
    """
    Document Permissions for
    :class:`ProtectPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job.ProtectPDFJob>`
    """

    def __init__(self):
        """
        Constructs a new :samp:`Permissions` instance.
        """
        self.__permissions_list = []

    def get_values(self):
        """
        :return: the intended set of document permissions values.
        :rtype: list
        """
        return self.__permissions_list

    @enforce_types
    def add_permission(self, permission: Permission):
        """
        Adds a document :class:`Permission<adobe.pdfservices.operation.pdfjobs.params.protect_pdf.permission.Permission>`
        in the permissions set.

        :param permission: A document permission; can not be None.
        :type permission: Permission
        """
        self.__permissions_list.append(permission.__str__())
        return self
