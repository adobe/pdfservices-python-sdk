# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

class ServiceUsageException(Exception):
    """
    ServiceUsageError is thrown when either service usage limit has been reached or credentials quota has been exhausted.
    """

    DEFAULT_STATUS_CODE = 429
    """The default value of status code if there is no status code for this service failure."""

    DEFAULT_ERROR_CODE = 'UNKNOWN'
    """The default value of error code if there is no status code for this service failure."""

    def __init__(self, message, request_tracking_id, status_code=DEFAULT_STATUS_CODE, error_code=DEFAULT_ERROR_CODE):
        self.message = message
        self._request_tracking_id = request_tracking_id
        self._status_code = status_code if status_code else self.DEFAULT_STATUS_CODE
        self._error_code = error_code if error_code else self.DEFAULT_ERROR_CODE

    def __str__(self):
        return "description ={description}; requestTrackingId={request_id}; statusCode={status_code}; errorCode={error_code}".format(description=self.message,
                                                                                                                                     request_id=self.request_tracking_id,
                                                                                                                                     status_code=self.status_code,
                                                                                                                                     error_code=self.error_code)

    @property
    def request_tracking_id(self):
        """ The request tracking id of the exception."""
        return self._request_tracking_id

    @property
    def status_code(self):
        """ Returns the HTTP Status code or DEFAULT_STATUS_CODE if the status code doesn't adequately represent the error."""
        return self._status_code

    @property
    def error_code(self):
        """ Returns the detailed message of this error."""
        return self._error_code


class ServiceApiException(Exception):
    """ServiceApiException is thrown when an underlying service API call results in an error."""

    DEFAULT_STATUS_CODE = 0
    """The default value of status code if there is no status code for this service exception."""

    DEFAULT_ERROR_CODE = 'UNKNOWN'
    """Returns the HTTP Status code or DEFAULT_STATUS_CODE if the status code doesn't adequately represent the error."""

    def __init__(self, message, request_tracking_id, status_code=DEFAULT_STATUS_CODE, error_code=DEFAULT_ERROR_CODE):
        self.message = message
        self._request_tracking_id = request_tracking_id
        self._status_code = status_code if status_code else self.DEFAULT_STATUS_CODE
        self._error_code = error_code if error_code else self.DEFAULT_ERROR_CODE

    def __str__(self):
        return "description ={description}; requestTrackingId={request_id}; statusCode={status_code}; errorCode={error_code}".format(description=self.message,
                                                                                                                                     request_id=self.request_tracking_id,
                                                                                                                                     status_code=self.status_code,
                                                                                                                                     error_code=self.error_code)

    @property
    def request_tracking_id(self):
        """ The request tracking id of the exception."""
        return self._request_tracking_id

    @property
    def status_code(self):
        """ Returns the HTTP Status code or DEFAULT_STATUS_CODE if the status code doesn't adequately represent the error."""
        return self._status_code

    @property
    def error_code(self):
        """ Returns the detailed message of this error."""
        return self._error_code


class SdkException(Exception):
    """SdkException is typically thrown for client-side or network errors."""

    def __init__(self, message, request_tracking_id=None):
        self.message = message
        self._request_tracking_id = request_tracking_id

    def __str__(self):
        return "description ={description}, requestTrackingId={request_id}".format(description=self.message,
                                                                                   request_id=self.request_tracking_id)

    @property
    def request_tracking_id(self):
        """ The request tracking id of the exception."""
        return self._request_tracking_id
