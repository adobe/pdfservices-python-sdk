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


class JSONHintEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'json_hint'):
            dict_to_return = {}
            for fieldObj in obj.json_hint:
                field = fieldObj
                dict_field = obj.json_hint[field]
                if isinstance(dict_field, dict):
                    dict_field = dict_field['name']
                field_val = getattr(obj, field, None)
                if isinstance(field_val, str):
                    dict_to_return[dict_field] = field_val
                elif isinstance(field_val, list):
                    result = []
                    for list_element in field_val:
                        if isinstance(field_val, str):
                            result.append(list_element)
                        else:
                            result.append(json.loads(json.dumps(list_element, cls=JSONHintEncoder)))
                    dict_to_return[dict_field] = result
                else:
                    if field_val is not None:
                        dict_to_return[dict_field] = json.loads(json.dumps(field_val, cls=JSONHintEncoder))
            return dict_to_return
        return json.JSONEncoder.default(self, obj)


class JSONHintDecoder:

    @staticmethod
    def rev(dct):
        result = {}
        for key, val in dct.items():
            cls_type = str
            rev_key = val
            if isinstance(val, dict):
                cls_type = val['type']
                rev_key = val['name']
            result[rev_key] = [key, cls_type]
        return result

    @staticmethod
    def as_class(dct):
        reverse_map = JSONHintDecoder.rev(getattr(JSONHintDecoder.current_class, 'json_hint'))
        obj = JSONHintDecoder.current_class()
        for key, val in dct.items():
            if key in reverse_map:
                child_class = reverse_map[key][1]
                class_attr = reverse_map[key][0]
                if isinstance(val, dict):
                    JSONHintDecoder.current_class = child_class
                    setattr(obj, class_attr, JSONHintDecoder.as_class(val))
                else:
                    if isinstance(val, (int, str, bool)):
                        setattr(obj, class_attr, val)
                    else:
                        result = []
                        for lobj in val:
                            if not isinstance(lobj, dict):
                                result.append(lobj)
                            else:
                                JSONHintDecoder.current_class = child_class
                                result.append(JSONHintDecoder.as_class(lobj))
                        setattr(obj, class_attr, result)
        if hasattr(obj, 'post_process'):
            getattr(obj, 'post_process')()
        return obj
