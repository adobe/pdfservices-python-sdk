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


custom_error_messages = {

    # Custom IMS error messages
    "imsInvalidTokenGenericErrorMessage": 'Either your certificate for PDF Services API credentials has expired or an ' +
                                          'invalid Organization_ID/Account_ID has been used in credentials. Please visit Adobe IO ' +
                                          'Console(http://console.adobe.io/) to update your public certificate to use the same credentials or to check ' +
                                          'the value of Organization Id or Account ID.',
    "imsCertificateExpiredErrorMessage": 'Your certificate for PDF Services API credentials might have expired. ' +
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
    OPERATION_RESULT_TEMP_DIRECTORY = 'sdk_result'
    EXTRACT_OPERATION_NAME = "EXTRACT_PDF"
    AUTOTAG_OPERATION_NAME = "AUTOTAG_PDF"
    CREATE_OPERATION_NAME = "CREATE_PDF"
    DOCUMENT_MERGE_OPERATION_NAME = "DOCUMENT_MERGE"
    ESEAL_PDF_NAME = "ESEAL_PDF"
    PROTECT_PDF_NAME = "PROTECT_PDF"
    COMBINE_PDF_NAME = "COMBINE_PDF"
    EXPORT_PDF_OPERATION_NAME = "EXPORT_PDF"
    OCR_PDF_OPERATION_NAME = "OCR_PDF"
    HTML_TO_PDF_OPERATION_NAME = "HTML_TO_PDF"
    COMPRESS_PDF_OPERATION_NAME = "COMPRESS_PDF"
    LINEARIZE_PDF_OPERATION_NAME = "LINEARIZE_PDF"
    REMOVE_PROTECTION_OPERATION_NAME = "REMOVE_PROTECTION"
    PDF_TO_IMAGES_OPERATION_NAME = "PDF_TO_IMAGES"
    INSERT_PAGES_OPERATION_NAME = "INSERT_PAGES"
    REPLACE_PAGES_OPERATION_NAME = "REPLACE PAGES"
    REORDER_PAGES_OPERATION_NAME = "REORDER_PAGES"
    DELETE_PAGES_OPERATION_NAME = "DELETE_PAGES"
    ROTATE_PAGES_OPERATION_NAME = "ROTATE_PAGES"
    SPLIT_PDF_OPERATION_NAME = "SPLIT_PDF"
    PDF_PROPERTIES_OPERATION_NAME = "PDF_PROPERTIES"
