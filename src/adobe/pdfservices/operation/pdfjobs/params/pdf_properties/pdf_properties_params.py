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
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class PDFPropertiesParams(PDFServicesJobParams):
    """
    Parameters for getting properties of a PDF using
    :class:`PDFPropertiesJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_properties_job.PDFPropertiesJob>`
    """

    @enforce_types
    def __init__(self, *, include_page_level_properties: bool = False):
        """
        Constructs a new :samp:`PDFPropertiesParams`.

        :param include_page_level_properties: If true, the page level properties of the input PDF will be included in
            the resulting JSON file or JSON Object. (Optional, use key-value)
        :type include_page_level_properties: bool
        """
        self._include_page_level_properties = include_page_level_properties

    def get_include_page_level_properties(self):
        """
        :return: Page level properties
        :rtype: bool
        """
        return self._include_page_level_properties
