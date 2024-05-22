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


class AutotagPDFParams(PDFServicesJobParams):
    """
    Parameters for creating a tagged PDF using
    :class:`AutotagPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.autotag_pdf_job.AutotagPDFJob>`.
    """

    @enforce_types
    def __init__(self, *, shift_headings: bool = False, generate_report: bool = False):
        """
        Constructs a new instance of :samp:`AutotagPDFParams`.

        :param generate_report: If true, generates an additional tagging report which contains the information about the
         tags that the tagged output PDF document contains.(Optional, use key-value)
        :type generate_report: bool
        :param shift_headings: If true, then the headings will be shifted in the output PDF document. (Optional, use key-value)
        :type shift_headings: bool
        :return: A new instance of AutotagPDFParams
        :rtype: AutotagPDFParams
        """
        self._shift_headings = shift_headings
        self._generate_report = generate_report

    def get_shift_headings(self):
        """
        :return: A boolean value specifying whether headings need to be shifted in the tagged PDF.
        :rtype: bool
        """
        return self._shift_headings

    def get_generate_report(self):
        """
        :return: A boolean value specifying whether an additional tagging report needs to be generated.
        :rtype: bool
        """
        return self._generate_report
