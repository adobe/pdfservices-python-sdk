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

from functools import wraps
from typing import Callable, Any, Tuple


def enforce_types(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Tuple[Any], **kwargs: Any):
        # Get the argument names and types from function annotations
        arg_types = func.__annotations__

        # Check positional arguments starting from the second one (the first one is 'self' or 'cls' for instance
        # methods and class methods, respectively)
        for i, arg in enumerate(args[1:]):
            arg_name = list(arg_types.keys())[i]
            if arg_name in arg_types and arg_types[arg_name] != Any and not isinstance(arg, arg_types[arg_name]):
                raise TypeError(f"Argument '{arg_name}' must be of type {arg_types[arg_name].__name__}")

        # Check keyword arguments
        for kwarg_name, kwarg_value in kwargs.items():
            if (kwarg_name in arg_types and arg_types[kwarg_name] != Any
                    and not isinstance(kwarg_value, arg_types[kwarg_name])):
                raise TypeError(f"Argument '{kwarg_name}' must be of type {arg_types[kwarg_name].__name__}")

        # Call the original function if type checks pass
        return func(*args, **kwargs)

    return wrapper
