# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/12/12 17:27
"""
import base64
import io
import math
import os

import cv2
import numpy as np
from PIL import Image
from faceRecognition.utils.loggers import logger


def image_base64_to_array(base64_data):
    img_b64decode = base64.b64decode(base64_data)
    image = io.BytesIO(img_b64decode)
    image_data = np.frombuffer(image.getvalue(), dtype=np.uint8)
    image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    # image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
    return image_data


def image_binary_to_array(binary_data):
    image = io.BytesIO(binary_data)
    image_data = np.frombuffer(image.getvalue(), dtype=np.uint8)
    image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return image_data


def image_array_to_image_binary(image_array):
    encode_image = cv2.imencode(".jpg", image_array)[1]
    byte_data = encode_image.tobytes()
    return byte_data


def image_array_to_base64(image_array):
    # img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    encode_image = cv2.imencode(".jpg", image_array)[1]
    byte_data = encode_image.tobytes()
    base64_str = base64.b64encode(byte_data).decode("utf-8")  # 转换为base64
    return base64_str


def image_data_resize(image_data, new_image_size):
    _shape = image_data.shape
    b_id_card_wh = new_image_size[0] * new_image_size[1]
    alpha = math.sqrt(b_id_card_wh / (_shape[0] * _shape[1]))
    if alpha < 1:
        new_shape = [int(_shape[0] * alpha), int(_shape[1] * alpha), 3]
        image_data = cv2.resize(image_data, (new_shape[1], new_shape[0]), interpolation=cv2.INTER_AREA)
    return image_data


def save_array_to_file(image_array, file_name):
    s_img = Image.fromarray(image_array)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    s_img.save(file_name)


def image_file_to_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_data = base64.b64encode(image_file.read())
            # 将 bytes 转换为字符串
            encoded_string = encoded_data.decode("utf-8")
            return encoded_string
    except Exception as e:
        logger.info(f"the image path not exist: {image_path}")
        logger.info(e.__str__())
        return None
