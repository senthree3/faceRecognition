# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/7 11:19
"""

from django.utils.decorators import method_decorator
from .accessKeyCheckMiddleware import AccessKeyCheckMiddleware
from .dataEncryptDecryptMiddleware import DataEncryptDecryptMiddleware
from .responseMiddleware import ResponseMiddleware
from .signValidationMiddleware import SignValidationMiddleware


def apply_capability_middleware_decorator(view_func):
    capability_middleware = [
        ResponseMiddleware,
        AccessKeyCheckMiddleware,
        SignValidationMiddleware,
        DataEncryptDecryptMiddleware
    ]

    for m in capability_middleware[::-1]:
        view_func = method_decorator(m, name="dispatch")(view_func)

    return view_func
