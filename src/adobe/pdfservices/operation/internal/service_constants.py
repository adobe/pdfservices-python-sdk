# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

custom_error_messages = {

    # Custom IMS error messages
    "imsInvalidTokenGenericErrorMessage": 'Either your certificate for PDF Tools API credentials has expired or an ' +
                                          'invalid Organization_ID/Account_ID has been used in credentials. Please visit Adobe IO ' +
                                          'Console(http://console.adobe.io/) to update your public certificate to use the same credentials or to check ' +
                                          'the value of Organization Id or Account ID.',
    "imsCertificateExpiredErrorMessage": 'Your certificate for PDF Tools API credentials might have expired. ' +
                                         'Please visit Adobe IO Console(http://console.adobe.io/) to update your public certificate to use the same ' +
                                         'credentials.',

    # Service usage exception error messages
    "serviceUsageLimitReachedErrorMessage": 'Service usage limit has been reached. Please retry after sometime.',
    "integrationServiceUsageLimitReachedErrorMessage": 'Service usage limit has been reached for the integration. ' +
                                                       'Please retry after sometime.',

    # Quota specific exception error messages
    "quotaExhaustedErrorMessage": 'Free trial quota exhausted. Please visit (www.adobe.com/go/pdftoolsapi_err_quota) to ' +
                                  'upgrade to paid credentials.',
    "quotaUnavailableErrorMessage": 'Quota for this operation is not available. Please visit ' +
                                    '(www.adobe.com/go/pdftoolsapi_home) to start using free trial quota.'
}


class ServiceConstants:
    HTTP_CONNECT_TIMEOUT = 4000
    HTTP_READ_TIMEOUT = 10000
    HTTP_MAX_RETRIES = 1
    HTTP_RETRY_DELAY_FACTOR = 2
    HTTP_MAX_RETRYIN_TERVAL = 15000
    HTTP_RETRY_BACKOFF_INTERVAL = 3000
    HTTP_SUCCESS_RESPONSE_CODE = 200, 201, 202, 204
    HTTP_RETRIABLE_RESPONSE_CODE = 401
    APACHE_CLIENT_MAX_CONNECTION = 200
    APACHE_CLIENT_MAX_CONNECTION_PER_ROUTE = 20
    JWT_BASE_URI = 'https://ims-na1.adobelogin.com'
    JWT_URI_SUFFIX = 'ims/exchange/jwt/'
    JWT_AUDIENCE_SUFFIX = 'c/'
    JWT_CLAIM = 's/ent_documentcloud_sdk'
    OPERATION_RESULT_TEMP_DIRECTORY = 'extractSdkResult'
    CPF_OPS_CREATE_URI = 'https://cpf-ue1.adobe.io/ops/:create'
    CPF_OPS_EXTRACT_ANALYZER_ID = 'urn:aaid:cpf:58af6e2c-1f0c-400d-9188-078000185695'
    TEXT_MIME_TYPE = "text/directory"
    EXTRACT_OPERATION_NAME = "EXTRACT_PDF"
    CONTENT_ANALYZER_REQUESTS_STRING = "contentAnalyzerRequests"
    CONTENT_ANALYZER_RESPONSE_STRING = "contentAnalyzerResponse"
