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
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class RemoveProtectionParams(PDFServicesJobParams):
    """
    Parameters for removing protection from pdf using
    :class:`RemoveProtectionJob<adobe.pdfservices.operation.pdfjobs.jobs.remove_protection_job.RemoveProtectionJob>`
    """

    @enforce_types
    def __init__(self, password: str):
        """
        Constructs a new :samp:`RemoveProtectionParams` instance.

       :param password: the password to be used for removing protection from pdf.
       :type password: str
       :return: A new instance of RemoveProtectionParams
       :rtype: RemoveProtectionParams
       """
        self.__password = password
        ValidationUtil.validate_password_to_remove_protection(password)

    def get_password(self):
        """
        :return: Returns the password to be used for removing protection from pdf.
        :rtype: str
        """
        return self.__password
