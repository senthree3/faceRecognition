from django.test import TestCase
import requests
import base64
import uuid
import time
import json
from faceRecognition.utils.encryptDecryptAlgorithm.AesCrypt import aesCrypt
from faceRecognition.utils.customGenerateSign import CustomGenerateSign


# Create your tests here.


def face_register_test(burl, ak, sk):
    url = burl + "faceReg"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/ycy.jpg"
    # image_path = "/home/cv/zhouhs/datasets/smog_fire/images/smog_00005210.jpg"
    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image": base64_data_0[:20],
        "face_id": "000010000013",
        "user_name": "N3",
        "phone": None,
    }
    aes = aesCrypt(key=sk, key_size=32)
    data_e = aes.encrypt(json.dumps(data))
    sign = CustomGenerateSign(ak, sk).generate_sign(request_id, timestamp, data_e)
    json_data = {
        "data": data_e,
        "access_key": ak,
        "time_stamp": timestamp,
        "request_id": request_id,
        "sign": sign,
    }

    res = requests.post(url, json=json_data).json()
    print(res)
    res_data = aes.decrypt(res["data"])
    print(f"type:{type(res_data)} data info:", res_data)


def face_reg_delete_test(burl, ak, sk):
    url = burl + "faceRegDelete"
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "face_id": ["00000000010"],
    }
    aes = aesCrypt(key=sk, key_size=32)
    data_e = aes.encrypt(json.dumps(data))
    sign = CustomGenerateSign(ak, sk).generate_sign(request_id, timestamp, data_e)
    json_data = {
        "data": data_e,
        "access_key": ak,
        "time_stamp": timestamp,
        "request_id": request_id,
        "sign": sign,
    }

    res = requests.post(url, json=json_data).json()
    print(res)
    res_data = aes.decrypt(res["data"])
    print(f"type:{type(res_data)} data info:", res_data)


def face_reg_update_test(burl, ak, sk):
    url = burl + "faceRegUpdate"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/ycy2.jpg"
    # image_path = "/home/cv/zhouhs/datasets/smog_fire/images/smog_00005210.jpg"
    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image": base64_data_0,
        "face_id": "3322202401085678",
        "user_name": "test",
        "phone": "991",
    }
    aes = aesCrypt(key=sk, key_size=32)
    data_e = aes.encrypt(json.dumps(data))
    sign = CustomGenerateSign(ak, sk).generate_sign(request_id, timestamp, data_e)
    json_data = {
        "data": data_e,
        "access_key": ak,
        "time_stamp": timestamp,
        "request_id": request_id,
        "sign": sign,
    }

    res = requests.post(url, json=json_data).json()
    print(res)
    res_data = aes.decrypt(res["data"])
    print(f"type:{type(res_data)} data info:", res_data)


def face_reg_query_test(burl, ak, sk):
    url = burl + "faceRegQuery"
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "page": 1,
        "size": 20
    }
    aes = aesCrypt(key=sk, key_size=32)
    data_e = aes.encrypt(json.dumps(data))
    sign = CustomGenerateSign(ak, sk).generate_sign(request_id, timestamp, data_e)
    json_data = {
        "data": data_e,
        "access_key": ak,
        "time_stamp": timestamp,
        "request_id": request_id,
        "sign": sign,
    }

    res = requests.post(url, json=json_data).json()
    # print(res)
    res_data = json.loads(aes.decrypt(res["data"]))
    print(json.dumps(res_data))
    # print(len(res_data))
    # # print(f"type:{type(res_data)} data info:", res_data)


def face_reg_id_query_test(burl, ak, sk):
    url = burl + "faceRegIDQuery"
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "face_id": ["3322102401086990", "3322202401085279", "3322202401085679"],
    }
    aes = aesCrypt(key=sk, key_size=32)
    data_e = aes.encrypt(json.dumps(data))
    sign = CustomGenerateSign(ak, sk).generate_sign(request_id, timestamp, data_e)
    json_data = {
        "data": data_e,
        "access_key": ak,
        "time_stamp": timestamp,
        "request_id": request_id,
        "sign": sign,
    }

    res = requests.post(url, json=json_data).json()
    print(res)
    res_data = json.loads(aes.decrypt(res["data"]))
    print(json.dumps(res_data))
    # print(len(res_data))
    # print(f"type:{type(res_data)} data info:", res_data)


if __name__ == "__main__":
    _base_url = "http://10.73.135.102:8000/ai/openAbility/v1/"
    _ak = "8VPJvDtuLlxk864RAK4gizFMtEkMWfA0"
    _sk = "fMXKto3xLQOpEL58tYraXpwbEViH7iHH"
    # face_register_test(_base_url, _ak, _sk)
    # face_reg_delete_test(_base_url, _ak, _sk)
    face_reg_query_test(_base_url, _ak, _sk)
    # face_reg_id_query_test(_base_url, _ak, _sk)
    # face_reg_update_test(_base_url, _ak, _sk)
