# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/8 17:24
"""
import random
import string
import uuid


def generate_random_mixed_case_string(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_uuid4_string(horizontal_bar=True):
    uuid_str = uuid.uuid4()
    return str(uuid_str) if horizontal_bar else uuid_str.hex
