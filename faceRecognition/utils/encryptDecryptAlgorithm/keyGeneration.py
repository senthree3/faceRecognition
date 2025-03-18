# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2021/12/8 14:54
"""
import time
from Crypto.Random import random
from Crypto.Hash import MD5, SHA256


def key_generation(hash_type="MD5", digest_size=32):
    assert digest_size <= 32
    now = int(time.time_ns() / 1000)
    random_number = random.randrange(0, now)
    hash_data = str(random_number) + str(now)
    if hash_type == "SHA256":
        hash_key = SHA256.new(hash_data.encode()).hexdigest()
    else:
        hash_key = MD5.new(hash_data.encode()).hexdigest()
    return hash_key[:digest_size]


if __name__ == "__main__":
    t = key_generation()
    print(t)
