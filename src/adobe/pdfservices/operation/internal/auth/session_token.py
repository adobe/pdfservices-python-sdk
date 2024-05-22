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


from datetime import datetime, timedelta


class SessionToken:
    expired_at: datetime

    def __init__(self, access_token, expired_in_ms):
        self.access_token = access_token
        self.expired_at = (datetime.now() + timedelta(milliseconds=expired_in_ms)) if expired_in_ms is not None \
            else None
