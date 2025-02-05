# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 10:49
"""


class InterfaceException(Exception):
    def __init__(self, message, code):
        super(InterfaceException, self).__init__(message)
        self.code = code


class NormalErrorException(Exception):
    def __init__(self, message, code):
        super(NormalErrorException, self).__init__(message)
        self.code = code
