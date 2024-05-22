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
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.page_layout import PageLayout
from adobe.pdfservices.operation.pdfjobs.params.pdf_services_job_params import PDFServicesJobParams


class HTMLtoPDFParams(PDFServicesJobParams):
    """
    Parameters for converting HTML to PDF using
    :class:`HTMLtoPDFJob<adobe/pdfservices/operation/pdfjobs/jobs/html_to_pdf_job.HTMLtoPDFJob>`
    """

    @enforce_types
    def __init__(self, *,
                 json: str = '{}',
                 include_header_footer: bool = False,
                 page_layout: PageLayout = PageLayout()):
        """
        Constructs a new :samp:`HTMLtoPDFParams` instance.

        :param json: Sets the data to be used by the javascript in the source html file to manipulate the HTML DOM
            before it gets converted to PDF.
            This mechanism is intended to be used to supply data that might otherwise be retrieved using ajax requests.

            To make use of this mechanism, the source html file must include a script element such as:

            :literal:`<script src='./json.js' type='text/javascript'></script>`

            where json.js refers to the JSON data,</pre>
            And also Requires javascript in the source html file to make use of this JSON data to manipulate the HTML
            DOM. (Optional, use key-value)
        :type json: str
        :param include_header_footer: includeHeaderFooter parameter. If true, default header and footer will be included
            in resulting PDF.
                - The default header consists of the date and the document title.
                - The default footer consists of the file name and page number.
            (Optional, use key-value)
        :type include_header_footer: bool
        :param page_layout: Intended page layout of the resulting PDF file. (Optional, use key-value)
        :type page_layout: PageLayout
        """
        self.json = json
        self.include_header_footer = include_header_footer
        self.page_layout = page_layout

    def get_json(self):
        """
        :return: Returns JSON data that will be used to manipulate HTML DOM before it is converted into PDF file.
            This mechanism is intended to be used to supply data that might otherwise be retrieved using ajax requests.

            To make use of this mechanism, the source html file must include a script element such as:

            :literal:`<script src='./json.js' type='text/javascript'></script>`

            where json.js refers to the JSON data,</pre>
            And also Requires javascript in the source html file to make use of this JSON data to manipulate the HTML
            DOM.
        :rtype: str
        """
        return self.json

    def get_include_header_footer(self):
        """
        :return: Returns true if default header and footer will be included in the resulting PDF file.
            - The default header consists of the date and the document title.
            - The default footer consists of the file name and page number.
        :rtype: bool
        """
        return self.include_header_footer

    def get_page_layout(self):
        """
        :return: Intended page layout of the resulting PDF file.
        :rtype: bool
        """
        return self.page_layout
