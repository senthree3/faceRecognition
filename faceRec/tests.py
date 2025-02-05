import base64
import json
import time
import uuid

import requests
from django.test import TestCase

# Create your tests here.
from faceRecognition.utils import aesCrypt
from faceRecognition.utils.customGenerateSign import CustomGenerateSign


def face_feature_extraction_test(burl, ak, sk):
    url = burl + "faceFeatureExtraction"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/blm018876.jpg"
    # image_path = "/home/cv/zhouhs/datasets/smog_fire/images/smog_00005210.jpg"
    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image": base64_data_0,
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
    res_data = aes.decrypt(res["data"])
    print(res_data)
    # print(f"type:{type(res_data)} data info:", json.loads(res_data))


def o2o_image_recognition_test(burl, ak, sk):
    url = burl + "face11Images"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/ycy.jpg"
    image_path_1 = "/home/cv/zhouhs/projects/faceRecognition/testData/ycy2.jpg"
    # image_path = "/home/cv/zhouhs/datasets/smog_fire/images/smog_00005210.jpg"
    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')

    with open(image_path_1, 'rb') as f:
        base64_data_1 = base64.b64encode(f.read()).decode('utf-8')
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image1": base64_data_0,
        "image2": base64_data_1
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
    print(res_data)
    # print(f"type:{type(res_data)} data info:", json.loads(res_data))


def o2o_check_recognition_test(burl, ak, sk):
    url = burl + "face11Check"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/ccc1.png"
    # image_path = "/home/cv/zhouhs/datasets/smog_fire/images/smog_00005210.jpg"
    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')

    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image": base64_data_0,
        "face_id": "3322102401086990"
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
    print(res_data)
    # print(f"type:{type(res_data)} data info:", json.loads(res_data))


def o2n_recognition_recognition_test(burl, ak, sk):
    url = burl + "faceSimilarRetrieval"#"face1N"
    image_path = "/home/cv/zhouhs/projects/faceRecognition/testData/ycy.jpg"

    with open(image_path, 'rb') as f:
        base64_data_0 = base64.b64encode(f.read()).decode('utf-8')

    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    data = {
        "image": base64_data_0,
        "top_k": 5,
        "similar_face": True,
        # "det_image": True,
        # "drawn_image": True,
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
    # print(json.dumps(json_data))

    res = requests.post(url, json=json_data).json()
    # print(json.dumps(res))
    res_data = aes.decrypt(res["data"])
    print(res_data)
    # print(f"type:{type(res_data)} data info:", json.loads(res_data))


if __name__ == "__main__":
    _base_url = "http://10.73.135.102:8000/ai/openAbility/v1/"
    _ak = "8VPJvDtuLlxk864RAK4gizFMtEkMWfA0"
    _sk = "fMXKto3xLQOpEL58tYraXpwbEViH7iHH"
    # face_feature_extraction_test(_base_url, _ak, _sk)
    # o2o_image_recognition_test(_base_url, _ak, _sk)
    # o2o_check_recognition_test(_base_url, _ak, _sk)
    # time_s = time.time()
    o2n_recognition_recognition_test(_base_url, _ak, _sk)
    # print(f"spend time:{time.time() - time_s}")
    # import faiss
    # _index = faiss.IndexFlatIP(512)
    # _index = faiss.IndexIDMap(_index)
    # faiss.write_index()
