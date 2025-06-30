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
from typing import Dict, Any

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class ImportPDFFormDataParams(PDFServicesJobParams):
    """
    Parameters for importing form data into PDF using
    :class:`ImportPDFFormDataJob<adobe.pdfservices.operation.pdfjobs.jobs.import_pdf_form_data_job.ImportPDFFormDataJob>`
    """

    @enforce_types
    def __init__(self, json_form_fields_data: dict):
        """
        Constructs a new :samp:`ImportPDFFormDataParams` instance.

        :param json_form_fields_data: Dictionary containing form field data to import into the PDF.
            Keys should match the form field names in the target PDF, and values should be the data to fill.
        :type json_form_fields_data: dict
        """
        self.json_form_fields_data = json_form_fields_data

    def get_json_form_fields_data(self) -> Dict[str, Any]:
        """
        :return: Returns the form field data dictionary that will be imported into the PDF.
        :rtype: Dict[str, Any]
        """
        return self.json_form_fields_data

    def get_json_form_fields_data_string(self) -> str:
        """
        :return: Returns the form field data as a JSON string.
        :rtype: str
        """
        return json.dumps(self.json_form_fields_data) 