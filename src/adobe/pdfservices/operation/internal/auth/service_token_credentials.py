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

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.internal.constants.custom_error_messages import CustomErrorMessages
from adobe.pdfservices.operation.internal.util.string_util import StringUtil


class ServiceTokenCredentials(Credentials):
    def __init__(self, client_id: str, token: str):
        if StringUtil.is_blank(client_id):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Client ID"))
        if StringUtil.is_blank(client_id):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Token"))
        self._client_id = client_id
        self._token = token

    def get_client_id(self):
        return self._client_id

    def set_client_id(self, client_id):
        if StringUtil.is_blank(client_id):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Client ID"))
        self._client_id = client_id

    def get_token(self):
        return self._token

    def set_token(self, token):
        if StringUtil.is_blank(token):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Token"))
        self._token = token
