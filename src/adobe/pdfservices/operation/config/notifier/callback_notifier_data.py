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
from typing import Dict

from adobe.pdfservices.operation.config.notifier.notifier_data import NotifierData
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder
from adobe.pdfservices.operation.internal.util.string_util import StringUtil


class CallbackNotifierData(NotifierData):
    """
    Represents the configuration for the notifier data.
    """

    json_hint = {
        'url': 'url',
        'headers': 'headers'
    }
    """
    For JSON Representation of this class, used internally by SDK.
    """

    @enforce_types
    def __init__(self, url: str, *,
                 headers: Dict = None):
        """
        Constructs an instance of :samp:`CallbackNotifierData`.

        :param url: Callback URL, can not be None
        :type url: str
        :param headers: Callback headers. (Optional, use key-value)
        :type headers: dict
        """
        if StringUtil.is_blank(url):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("URL"))

        self.url = url
        self.headers = headers

    def to_json(self):
        """
        :return: Representation of CallbackNotifierData as a JSON string, used internally by the SDK.
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
