# 人脸识别服务接口文档

## 一、接口能力介绍

1. 人脸库管理能力：提供人脸身份信息注册、更新、查询、删除等用户自管理维护能力。
2. 人脸检测能力：通过上传人脸图像信息，检测图像中人脸目标，默认提取占比最大人脸，用户可自定义提取存在人脸数量。
3. 人脸特征提取能力：获取图像中人脸目标信息，并提取512维人脸特征空间向量特征。
4. 人脸1:1(图像)识别能力：比较两张人脸图像中最大人脸相似度，并判定为相同、相似、不同三种人脸类型维度之一。
5. 人脸1:1(校验)库识别能力：通过上传人脸图像，以及注册的人脸ID，比对图像人脸信息与注册ID人脸相似度信息。
6. 人脸1:N识别能力：获取图像人脸特征信息，并检索人脸库中是否存在该人脸注册信息，若存在则返回注册人脸ID等身份信息。
7. 相似人脸搜索能力：通过上传人脸图像，检索人脸库中与之相似人脸信息，最大检索Top5人脸注册数据信息。

注：所有能力使用接口信息均需获取access_key、secret_key对数据进行加解密验证；人脸库管理可使用web管理后台可视化能力，账号需注册

## 二、能力服务调用接口标准封装说明

### 1. 接口请求标准化参数说明

| 接口参数名 | 类型 | 描述说明 |
| --- | --- | --- |
| access_key | String | 访问密钥 |
| time_stamp | String | 时间戳，unix timestamp，可做为防止重复攻击字段，到毫秒 |
| request_id | String | 请求ID，使用uuid4字符串 |
| sign | String | 签名值，见约定签名规则 |
| data | Base64 | 加密数据，见加密规则 |

| 请求头参数 | 值 |
| --- | --- |
| Content-Type | application/json |

#### 签名生成规则（sign）
sign=f"{access_key}&{secret_key}&{request_id}&{time_stamp}&{data}"的MD5值

#### 数据加密算法（data）
使用AES（Advanced Encryption Standard）对称加密算法，CBC（Cipher Block Chaining）工作模式，密钥（key）为secret_key，初始向量（IV）为secret_key前16位字符串，填充模式（Padding）使用PKCS#7。

#### 接口标准化请求式例
```json
{
  "data": "025jNUOsLQuk...GXPaa/Yw",
  "access_key": "8VPJvDtuLlxk864RAK4gizFMtEkMWfA0",
  "time_stamp": "1705392729703",
  "request_id": "109942d8-048e-45e5-b78c-0b66eff4f224",
  "sign": "8dc2757a3531893c9de124054814a310"
}
```

#### 能力接口请求base地址
http://{IP}:{PORT}/ai/openAbility/v1/

### 2. 接口返回参数标准化说明

| 参数名 | 类型 | 描述说明 |
| --- | --- | --- |
| code | Int | 请求状态码 |
| message | String | 请求状态信息说明 |
| request_id | String | 请求ID，返回请求对应request_id |
| data | Base64 | 请求接口返回加密数据，需解密，若出现错误则无该参数 |

#### 接口标准化返回式例
```json
{
  "data": "IuvaXSzZTp...uoUXnkaiuItKu\nYeWt\n",
  "code": 200,
  "message": "success",
  "request_id": "abc12aa1-12d0-4020-8759-d2fcb21ca92d"
}
```

#### 接口常见状态码说明

| 状态码（code） | 消息描述（message） | 说明 |
| --- | --- | --- |
| 200 | success | 成功 |
| 500 | fail | 失败 |
| 400 | Missing required parameters | 缺少必要参数 |
| 401 | Invalid access key | 无效的访问密钥 |
| 402 | Invalid sign | 无效签名 |
| 6001 | Encrypted data format error | 加密数据格式错误 |
| 7521 | Ability not subscription | 能力未订阅 |
| 7522 | Ability not exist | 能力不存在 |
| 7523 | Ability subscription has expired | 能力订阅已过期 |
| 7524 | Exhausted maximum request limit | 能力订阅已超过最大使用请求上限 |
| 7525 | Invalid request data format | 无效请求数据格式 |

#### 人脸相关状态码说明

| 状态码（code） | 消息描述（message） | 说明 |
| --- | --- | --- |
| 8301 | Face not found in image | 图像中不存在人脸 |
| 8401 | Face id registered | 人脸ID已注册 |
| 8402 | Faces with IDs do not exist | 人脸ID不存在 |
| 8403 | Face feature vector database do not exist | 人脸特征向量库存不存在 |

## 三、接口详细说明

### 1. 人脸库管理接口

#### (1) 人脸注册接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceReg

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片信息 |
| face_id | String | 是 | 人脸ID，不超过18个字符 |
| user_name | String | 是 | 姓名 |
| phone | String | 否 | 电话号码，不超过11个字符 |

请求样例：
```json
{
  "image": "/9j/4AAQSkZJRgABAQEA...",
  "face_id": "000000001",
  "user_name": "测试",
  "phone": null
}
```

返回参数data（布尔类型）：

| 类型 | 说明 |
| --- | --- |
| Boolean | True为注册成功 |

#### (2) 人脸删除接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceRegDelete

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| face_id | List | 是 | 人脸ID列表 |
| + | String | 是 | 人脸ID |

请求样例：
```json
{
  "face_id": [
    "00000000010"
  ]
}
```

返回参数data（布尔类型）：

| 类型 | 说明 |
| --- | --- |
| Boolean | True为注册成功 |

#### (3) 人脸更新接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceReg

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| face_id | String | 是 | 人脸ID |
| user_name | String | 否 | 新姓名 |
| phone | String | 否 | 新电话号码，不超过11个字符 |
| image | Base64 | 否 | 新人脸图片 |

请求样例：
```json
{
  "image": "/9j/4AAQSkZJRgABAQEA...",
  "face_id": "000000002",
  "user_name": "新测试",
  "phone": "10086"
}
```

返回参数data（布尔类型）：

| 类型 | 说明 |
| --- | --- |
| Boolean | True为注册成功 |

#### (4) 人脸ID查询接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceRegIDQuery

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| face_id | List | 是 | 人脸ID列表 |
| + | String | 是 | 人脸ID |

请求样例：
```json
{
  "face_id": [
    "000000002"
  ]
}
```

返回参数data（List）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| - | Dict | 是 | 人脸信息 |
| +face_id | String | 是 | 人脸ID |
| +user_name | String | 是 | 姓名 |
| +phone | String | 否 | 电话 |
| +image | Base64 | 是 | 人脸图像 |
| +feature | List | 是 | 人脸特征向量 |

返回样例：
```json
[
  {
    "face_id": "000000002",
    "user_name": "新测试",
    "phone": "10086",
    "image": "/9j/4AAQSkZJRg...z/9k=",
    "feature": [0.4183642268180847, -0.6539145112037659, ..., -0.06832651793956757]
  }
]
```

#### (5) 人脸分页查询接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceRegQuery

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| page | Int | 是 | 分页页码，默认为1 |
| size | Int | 是 | 每页查询数量，默认为20 |

请求样例：
```json
{
  "page": 1,
  "size": 20
}
```

返回参数data（List）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| - | Dict | 是 | 人脸信息 |
| +face_id | String | 是 | 人脸ID |
| +user_name | String | 是 | 姓名 |
| +phone | String | 否 | 电话 |
| +image | Base64 | 是 | 人脸图像 |
| +feature | List | 是 | 人脸特征向量 |

返回样例：
```json
[
  {
    "face_id": "000000002",
    "user_name": "新测试",
    "phone": "10086",
    "image": "/9j/4Aja...Isz/9k=",
    "feature": [
      0.4183642268180847,
      -0.06832651793956757
    ]
  },
  {
    "face_id": "000010000013",
    "user_name": "N3",
    "phone": null,
    "image": "/9j/4AAQS...j/2Q==",
    "feature": [
      -2.0406696796417236,
      -1.5759130716323853,
      -0.1332605928182602
    ]
  }
]
```

### 2. 人脸检测接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceDet

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片 |
| det_type | Int | 否 | 检测图像中人脸数据，0为所有人脸；1为默认值，即检测人脸占比最大人脸 |
| det_image | Boolean | 否 | 是否返回检测到的人脸图像，默认为false不返回，true为返回 |
| draw_image | Boolean | 否 | 是否返回原图人脸目标图像，默认为false不返回，true为返回 |

请求样例：
```json
{
  "image": "/9j/4AAQ...iG0ukJQlc8k//2Q==",
  "det_type": 1,
  "det_image": true,
  "draw_image": true
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| bbox | List | 是 | 检测人脸图像像素坐标列表 |
| + | List | 是 | 人脸xyxy像素坐标位置信息 |
| possibility | List | 是 | 人脸目标概率列表 |
| + | Float | 是 | 坐标区域对应存在人脸概率 |
| det_image | List | 否 | 检测到人脸图像列表 |
| + | Base64 | 否 | 截取的人脸目标图像 |
| draw_image | Base64 | 否 | 基于原图绘制人脸目标区域图像 |

返回样例：
```json
{
  "bbox": [
    [36,90,82,148]
  ],
  "possibility": [
    0.864
  ],
  "det_image": [
    "/9j/4AAQSkZJRgABAQAA..."
  ],
  "draw_image": "/9j/4AAQSkZJRgABAQAA..."
}
```

### 3. 人脸特征提取接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceFeatureExtraction

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片 |

请求样例：
```json
{
  "image": "/9j/4AAQ...iG0ukJQlc8k//2Q=="
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| feature | List | 是 | 人脸特征向量 |
| face_image | Base64 | 是 | 截取的人脸目标图像 |

返回样例：
```json
{
  "feature": [
    -0.6215987801551819,
    ...,
    1.034252643585205
  ],
  "face_image": "/9j/4AAQ...a6qKU726HNO5//9k="
}
```

### 4. 人脸1:1(图像)识别接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceFeatureExtraction

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image1 | Base64 | 是 | 图片1 |
| image2 | Base64 | 是 | 图片2 |

请求样例：
```json
{
  "image1": "/9j/4AAQ...iG0ukJQlc8k//2Q==",
  "image2": "/9j/4AAQ...iG0ukJQlc8k//2Q=="
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| possibility | Float | 是 | 人脸余弦相似度 |
| type | Int | 是 | 相似度类型1：likely_face；2：same_face；3：not_same_face |
| describe | String | 是 | 类型描述 |

返回样例：
```json
{
  "possibility": 0.456,
  "type": 2,
  "describe": "same_face"
}
```

### 5. 人脸1:1(校验)库识别接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceFeatureExtraction

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片 |
| face_id | String | 是 | 人脸ID |

请求样例：
```json
{
  "image": "/9j/4AAQ...iG0ukJQlc8k//2Q==",
  "face_id": "000000002"
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| possibility | Float | 是 | 人脸余弦相似度 |
| type | Int | 是 | 相似度类型1：likely_face；2：same_face；3：not_same_face |
| describe | String | 是 | 类型描述 |

返回样例：
```json
{
  "possibility": 0.653,
  "type": 2,
  "describe": "same_face"
}
```

### 6. 人脸1:N识别接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/face1N

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片 |
| det_image | Boolean | 否 | 是否返回检测到的人脸图像，默认为false不返回，true为返回 |
| draw_image | Boolean | 否 | 是否返回原图人脸目标图像，默认为false不返回，true为返回 |

请求样例：
```json
{
  "image": "/9j/4AAQ...iG0ukJQlc8k//2Q==",
  "det_image": true,
  "draw_image": true
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| possibility | Float | 是 | 人脸余弦相似度 |
| type | Int | 是 | 相似度类型0:unknown_face;1：likely_face；2：same_face |
| describe | String | 是 | 类型描述 |
| face_id | String | 是 | 人脸ID |
| user_name | String | 是 | 姓名 |
| phone | String | 否 | 电话 |
| det_image | Base64 | 否 | 截取的人脸图像 |
| draw_image | Base64 | 否 | 基于原图绘制人脸目标区域图像 |

返回样例：
```json
{
  "type": 2,
  "describe": "same_face",
  "face_id": "00000000013",
  "user_name": "测试",
  "phone": null,
  "possibility": 1.0,
  "det_image": "/9j/4AAQSkdH/2Q==",
  "draw_image": "/9j/4AAQSkZJJ+12Q=="
}
```

### 7. 相似人脸搜索接口
接口地址：http://{IP}:{PORT}/ai/openAbility/v1/faceSimilarRetrieval

请求参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| image | Base64 | 是 | 图片 |
| top_k | Int | 否 | 获取人脸库中topK个相似人脸，默认为1，最大为5 |
| similar_face | Boolean | 是 | 获取相似人脸必传true，若为false则同人脸1:N识别接口 |
| det_image | Boolean | 否 | 是否返回检测到的人脸图像，默认为false不返回，true为返回 |
| draw_image | Boolean | 否 | 是否返回原图人脸目标图像，默认为false不返回，true为返回 |

请求样例：
```json
{
  "image": "/9j/4AAQ...iG0ukJQlc8k//2Q==",
  "top_k": 2,
  "similar_face": true,
  "det_image": true,
  "draw_image": true
}
```

返回参数data（Json）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| similar_list | List | 是 | 相似度列表 |
| +possibility | Float | 是 | 人脸余弦相似度 |
| +type | Int | 是 | 相似度类型0:unknown_face;1：likely_face；2：same_face |
| +describe | String | 是 | 类型描述 |
| +face_id | String | 是 | 人脸ID |
| +user_name | String | 是 | 姓名 |
| +phone | String | 否 | 电话 |
| +rank | Int | 是 | 相似度排名 |
| det_image | Base64 | 否 | 截取的人脸图像 |
| draw_image | Base64 | 否 | 基于原图绘制人脸目标区域图像 |

返回样例：
```json
{
  "similar_list": [
    {
      "possibility": 0.091,
      "type": 3,
      "describe": "not_same_face",
      "face_id": "000000000001",
      "user_name": "测试",
      "phone": "991",
      "rank": 2
    },
    {
      "possibility": 1.0,
      "type": 2,
      "describe": "same_face",
      "face_id": "00000000013",
      "user_name": "N3",
      "phone": null,
      "rank": 1
    }
  ],
  "det_image": "/9j/4AAQSkdH/2Q==",
  "draw_image": "/9j/4AAQSkZJJ+12Q=="
}
```
