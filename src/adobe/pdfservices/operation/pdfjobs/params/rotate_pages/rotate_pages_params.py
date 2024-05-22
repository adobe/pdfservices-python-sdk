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

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_actions import PageActions
from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.rotate_page_action import \
    RotatePageAction
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams
from adobe.pdfservices.operation.pdfjobs.params.rotate_pages.angle import Angle


class RotatePagesParams(PDFServicesJobParams):
    """
    Parameters to rotate pages of a pdf using
    :class:`RotatePagesJob<adobe.pdfservices.operation.pdfjobs.jobs.rotate_pages_job.>RotatePagesJob`
    """

    def __init__(self):
        self.__page_actions: PageActions = PageActions()

    @enforce_types
    def add_angle_to_rotate(self, angle: Angle):
        """
        Sets the Angle to be used for rotating pages.

        :param angle: Angle; can not be None.
        :type angle: Angle
        """
        self.__page_actions.add_action(RotatePageAction(page_ranges=PageRanges().add_all(), rotation_angle=angle))
        return self

    @enforce_types
    def add_angle_to_rotate_for_page_ranges(self, angle: Angle, page_ranges: PageRanges):
        """
        Sets the Angle to be used for rotating pages specified in PageRanges.

        :param angle: Angle; can not be None.
        :type angle: Angle
        :param page_ranges: PageRanges; can not be None.
        :type page_ranges: PageRanges
        """
        page_ranges.validate()
        self.__page_actions.add_action(RotatePageAction(page_ranges=page_ranges, rotation_angle=angle))
        return self

    def get_page_actions(self):
        """
        :return: PageActions to be used for rotating pages.
        :rtype: PageActions
        """
        return self.__page_actions
