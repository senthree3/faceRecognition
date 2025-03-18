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