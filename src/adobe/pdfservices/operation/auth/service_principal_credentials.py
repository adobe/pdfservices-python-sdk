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
from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.internal.util.string_util import StringUtil


class ServicePrincipalCredentials(Credentials):
    """
    Service Principal credentials allow your application to call PDF Services API. For getting the credentials,
    `Click Here <https://www.adobe.com/go/dcsdks_credentials?ref=getStartedWithServicesSdk>`_.
    """

    @enforce_types
    def __init__(self, client_id: str, client_secret: str):
        """
        Constructs an instance of :samp:`ServicePrincipalCredentials`.

        :param client_id: client ID for ServicePrincipalCredentials; can not be None or empty.
        :type client_id: str
        :param client_secret: client secret for ServicePrincipalCredentials; can not be None or empty.
        :type client_secret: str
        """
        if StringUtil.is_blank(client_id):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Client ID"))
        if StringUtil.is_blank(client_secret):
            raise ValueError(CustomErrorMessages.GENERIC_CAN_NOT_BE_NONE_OR_EMPTY.format("Client Secret"))

        self.__client_id: str = client_id
        self.__client_secret: str = client_secret

    def get_client_id(self):
        """
        :return: Client Id
        :rtype: str
        """
        return self.__client_id

    def get_client_secret(self):
        """
        :return: Client Secret
        :rtype: str
        """
        return self.__client_secret
