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

from adobe.pdfservices.operation.config.notifier.notifier_data import NotifierData
from adobe.pdfservices.operation.config.notifier.notifier_type import NotifierType
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.json_hint_encoder import JSONHintEncoder


class NotifierConfig:
    """
    Represents the configuration for a notifier to be used to notify user about the completion of a
    :class:`PDFServicesJob<adobe.pdfservices.operation.pdf_services_job.PDFServicesJob>`.
    """

    json_hint = {
        'notifier_type': 'type',
        'notifier_data': 'data'
    }
    """
    For JSON Representation of this class, used internally by SDK.
    """

    @enforce_types
    def __init__(self, notifier_type: NotifierType, notifier_data: NotifierData):
        """
        Constructs an instance of :samp:`NotifierConfig`.

        :param notifier_type: specifies the type of notifier; can not be None.
        :type notifier_type: NotifierType
        :param notifier_data: encapsulates callback notifier data; can not be None.
        :type notifier_data: NotifierData
        """
        self.notifier_type = notifier_type.value
        self.notifier_data = notifier_data

    def to_json(self):
        """
        :return: representation of NotifierConfig as a JSON string, used internally by the SDK.
        :rtype: str
        """
        return json.dumps(self, cls=JSONHintEncoder, indent=1, sort_keys=True)
