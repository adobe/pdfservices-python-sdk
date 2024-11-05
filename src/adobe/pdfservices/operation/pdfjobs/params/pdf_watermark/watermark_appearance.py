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
from typing import Optional
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.exception.exceptions import SdkException
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class WatermarkAppearance:
    """
    Parameters to Watermark pdf using
    :class:`PDFWatermarkJob<adobe.pdfservices.operation.pdfjobs.jobs.pdf_watermark_job.PDFWatermarkJob>`.
    """
    json_hint = {
        'appear_on_foreground': 'appearOnForeground',
        'opacity': 'opacity'
    }

    @enforce_types
    def __init__(self, *, appear_on_foreground: Optional[bool] = True, opacity: Optional[int] = 100):
        """
        Constructs a new :samp:`WatermarkAppearance` instance.

        :param appear_on_foreground: Placement of watermark on the page. Watermark will be either foreground or background on the page. Default is foreground. (Optional, use key-value)
        :type appear_on_foreground: boolean
        :param opacity: opacity; Percentage value specifying watermark opacity. Specified as an Integer value from 0 to 100. (Optional, use key-value)
        :type page_count: int
        :return: A new instance of PDFWatermarkParams
        :rtype: PDFWatermarkParams
        """
        self.appear_on_foreground = appear_on_foreground
        if opacity is not None and (opacity < 0 or opacity > 100):
            raise SdkException("Opacity should be between 0 and 100")
        else:
            self.opacity = opacity

    def get_appear_on_foreground(self):
        """
        :return: Placement of watermark on the page. Watermark will be either foreground or background on the page. Default is foreground.
        :rtype: boolean
        """
        return self.appear_on_foreground

    def get_opacity(self):
        """
        :return: Percentage value specifying watermark opacity. Specified as an Integer value from 0 to 100 in SDK docs for opacity
        :rtype: number
        """
        return self.opacity

    def to_json(self):
        """
        Used internally by this SDK, not intended to be called by clients.
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)