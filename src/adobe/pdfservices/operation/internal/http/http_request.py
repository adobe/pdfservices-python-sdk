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

from adobe.pdfservices.operation.config.proxy.proxy_server_config import ProxyServerConfig
from adobe.pdfservices.operation.internal.auth.authenticator import Authenticator
from adobe.pdfservices.operation.internal.http.http_method import HttpMethod


class HttpRequest:

    # (url, data/files, headers, authenticator (if none its not authenticated), socket_timeout, connect_timeout)
    def __init__(self, http_method: HttpMethod, request_key: str, url: str, headers: dict, data=None, files=None,
                 authenticator: Authenticator = None, read_timeout=None, connect_timeout=None, retryable: bool = False,
                 proxies: ProxyServerConfig = None):
        self.method = http_method
        self.request_key = request_key
        self.url = url
        self.headers = headers
        self.data = data
        self.files = files
        self.authenticator = authenticator
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout
        self.retryable = retryable
        self.proxies = proxies
