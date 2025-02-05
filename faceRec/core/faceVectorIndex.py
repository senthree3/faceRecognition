# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/2 14:16
"""
import copy
import os
from typing import List

import faiss
import numpy as np
import time


class FaceVectorIndex(object):
    def __init__(self, dimension=512, index_file=None, save_interval=3600):
        self.dimension = dimension
        self.gpu_resources = faiss.StandardGpuResources()  # 使用GPU资源，如果可用
        self.gpu_device = 0
        self.index = None
        self.save_interval = save_interval  # 保存索引的时间间隔（秒）
        self.last_save_time = time.time()
        self.get_num_gpus = 0#faiss.get_num_gpus()

        self.index_file = index_file if index_file is not None else "index.index"

        if index_file is not None and os.path.isfile(self.index_file):
            self.load_index(index_file)
        else:
            self.init_index()

    def init_index(self):
        self.index = faiss.IndexFlatIP(self.dimension)  # 使用余弦相似度
        self.index = faiss.IndexIDMap(self.index)
        if self.get_num_gpus > 0:
            self.index = faiss.index_cpu_to_gpu(self.gpu_resources, self.gpu_device, self.index)  # 将索引移到GPU

    def add_face_vector(self, user_id, face_vector):
        """
        添加人脸向量到索引，关联用户ID和向量信息。
        """
        self.index.add_with_ids(np.array(face_vector), np.array([user_id]))
        # 检查是否应该保存索引
        self.check_and_save_index()

    def update_face_vector(self, user_id, new_face_vector):
        """
        更新指定用户的人脸向量信息。
        """
        if self.get_num_gpus > 0:
            tmp_index = faiss.index_gpu_to_cpu(self.index)
            tmp_index.remove_ids(np.array([user_id]))
            tmp_index.add_with_ids(np.array(new_face_vector), np.array([user_id]))
            tmp_index = faiss.index_cpu_to_gpu(self.gpu_resources, self.gpu_device, tmp_index)
            # self.index.remove_ids(np.array([user_id]))
        else:
            tmp_index = copy.deepcopy(self.index)
            tmp_index.remove_ids(np.array([user_id]))
            tmp_index.add_with_ids(np.array(new_face_vector), np.array([user_id]))
        self.index = tmp_index
        # 检查是否应该保存索引
        self.check_and_save_index()

    def search_face_vector(self, query_vector, k=5):
        """
        查询最接近的人脸向量，返回最接近的几个向量ID和向量信息。
        """
        D, I = self.index.search(np.array(query_vector), k)  # distance index
        return D[0].tolist(), I[0].tolist()

    def remove_face_vector(self, user_id: List):
        """
        删除指定用户的人脸向量信息。
        """
        if self.get_num_gpus > 0:
            tmp_index = faiss.index_gpu_to_cpu(self.index)
            tmp_index.remove_ids(np.array(user_id))
            tmp_index = faiss.index_cpu_to_gpu(self.gpu_resources, self.gpu_device, tmp_index)
            # self.index.remove_ids(np.array([user_id]))
        else:
            tmp_index = copy.deepcopy(self.index)
            tmp_index.remove_ids(np.array(user_id))
        self.index = tmp_index

        # 检查是否应该保存索引
        self.check_and_save_index()

    def save_index(self, index_file=None):
        """
        将索引保存到磁盘文件。
        """
        save_index_file = index_file if index_file is not None else self.index_file
        save_index = faiss.index_gpu_to_cpu(self.index) if self.get_num_gpus > 0 else self.index
        faiss.write_index(save_index, save_index_file)
        self.last_save_time = time.time()

    def load_index(self, index_file):
        """
        从磁盘文件加载索引。
        """
        self.index = faiss.read_index(index_file)
        if self.get_num_gpus > 0:
            self.index = faiss.index_cpu_to_gpu(self.gpu_resources, self.gpu_device, self.index)

    def check_and_save_index(self):
        """
        检查是否应该保存索引，如果满足保存条件，则执行保存操作。
        """
        current_time = time.time()
        if current_time - self.last_save_time >= self.save_interval:
            self.save_index(self.index_file)


# 示例用法
if __name__ == "__main__":
    pass

    #     import os
    #     import cv2
    #     import numpy as np
    #     import torch
    #     import random
    #     from recognition.arcface_torch.backbones import get_model
    #
    #     net_name = "mbf"
    #     net_weight = f"../work_dirs/ms1mv2_{net_name}_expand/model.pt"
    #     net = get_model(net_name, fp16=False)
    #     net.load_state_dict(torch.load(net_weight))
    #
    #     # face vector index
    # test_index_file = "test.index"
    # fvi = FaceVectorIndex(512)
    # # fvi.save_index(test_index_file)
    # for i in range(5):
    #     fvi.add_face_vector(124 + i, np.expand_dims(np.random.random(512), axis=0).astype('float32'))  # (1, 512)
    # print(fvi.index.ntotal)

#
#     face_dir = "/data2/datasets/face/expand_ms1mv2_face_z"
#
#
#     #
#     @torch.no_grad()
#     def test_face_index():
#         # 1. 设置文件夹路径和模型
#         # 您的人脸数据集文件夹路径
#
#         # 2. 遍历文件夹，加载人脸图像和标签
#         image_data = []
#         labels = []
#         user_list = os.listdir(face_dir)
#         # 随机挑选2000
#         random.shuffle(user_list)
#         tmp_user_list = []
#         t_u_count = 0
#         for user_dir in user_list:
#             user_path = os.path.join(face_dir, user_dir)
#             if len(os.listdir(user_path)) > 3:
#                 tmp_user_list.append(user_dir)
#                 t_u_count += 1
#             if t_u_count > 3:
#                 break
#         user_list = tmp_user_list
#
#         # user_list = user_list[:2000]
#         for user_dir in user_list:
#             user_path = os.path.join(face_dir, user_dir)
#             if os.path.isdir(user_path):
#                 label = user_dir  # 假设用户文件夹名称是标签
#                 tmp_image_list = os.listdir(user_path)
#                 tmp_image_list.sort()
#                 standard_face_image_path = os.path.join(user_path, tmp_image_list[-1])
#                 # for image_name in os.listdir(user_path):
#                 #     image_path = os.path.join(user_path, image_name)
#                 image = cv2.imread(standard_face_image_path)  # image_path)
#                 # --
#                 image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#                 image = np.transpose(image, (2, 0, 1))
#                 image = torch.from_numpy(image).unsqueeze(0).float()
#                 image.div_(255).sub_(0.5).div_(0.5)
#
#                 image_data.append(image)
#                 labels.append(label)
#
#         # 3. 提取特征向量
#         features = []  # 存储特征向量
#         for image in image_data:
#             # 使用您的人脸识别模型提取特征向量
#             net.eval()
#             feature_vector = net(image).numpy()
#             features.append(feature_vector)
#
#         # print(features)
#         # print(labels)
#         # for i in range(len(features)):
#         #     fvi.add_face_vector(user_id=int(labels[i]), face_vector=features[i])
#
#
#     @torch.no_grad()
#     def test_v_i(user_id):
#         u_d = os.path.join(face_dir, user_id)
#         v_i_image_list = os.listdir(u_d)
#         v_i_image_list.sort()
#         for t_img in v_i_image_list[:-2]:
#             t_img_path = os.path.join(u_d, t_img)
#             image = cv2.imread(t_img_path)  # image_path)
#             # --
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             image = np.transpose(image, (2, 0, 1))
#             image = torch.from_numpy(image).unsqueeze(0).float()
#             image.div_(255).sub_(0.5).div_(0.5)
#             net.eval()
#             feature_vector = net(image).numpy()
#             fvi.search_face_vector(feature_vector, k=3)
#
#
#     test_v_i("126211")
#     # test_face_index()
#     # fvi.save_index()
#
# # ['144840', '126214', '156917', '113534']
