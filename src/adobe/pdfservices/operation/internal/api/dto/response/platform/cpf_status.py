# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
import json


class CPFStatus(json.JSONDecoder):

    json_hint = {
        'completed' : 'completed',
        'type' : 'type',
        'status' : 'status',
        'report' : 'report',
        'title' : 'title'
    }

    def __init__(self, completed = None, type= None, status= None, report= None, title= None):
        self.completed = completed
        self.type = type
        self.status = status
        self.report = report
        self.title = title

