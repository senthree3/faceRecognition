# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2024/1/9 14:28
"""
import os
from typing import Dict, List

import numpy as np

from faceRecognition.enums import FaceRecStatusParameter
from faceRecognition.utils.customException import NormalErrorException
from faceRecognition.settings import FEATURE_DB_DIR, FEATURE_DB_REAL_TIME_UPDATE, FEATURE_DB_INIT_FILE
from faceMgt.core.getTenantFaceFeature import GetTenantFaceFeature
from .faceVectorIndex import FaceVectorIndex
from faceRecognition.utils.loggers import logger


class GlobalFeatureVectorPool(object):
    def __init__(self):
        self.tenant_feature_vectors: Dict[str, FaceVectorIndex] = {}

    def load_all_tenants_feature_vectors(self):
        # 在服务启动时加载所有租户的特征向量
        # 例如，从数据库中加载数据
        # 文件加载
        os.makedirs(FEATURE_DB_DIR, exist_ok=True)
        feature_db_list = os.listdir(FEATURE_DB_DIR)

        # 数据库加载
        gtff = GetTenantFaceFeature()
        tff = gtff.get_all_tenant_face_feature()
        for ta in tff.keys():
            fdb_name = f"{ta}.db"
            index_file = os.path.join(FEATURE_DB_DIR, fdb_name)
            if (fdb_name in feature_db_list) and FEATURE_DB_INIT_FILE:
                self.tenant_feature_vectors[ta] = FaceVectorIndex(index_file=index_file)
                logger.info(f"feature vector index load {fdb_name} success")
            else:
                if os.path.exists(index_file):
                    os.remove(index_file)
                    logger.info(f"remove old index file:{index_file}")
                fv = FaceVectorIndex(index_file=index_file)
                for ff_id, ff_a in tff[ta]:
                    fv.add_face_vector(user_id=int(ff_id),
                                       face_vector=np.expand_dims(np.array(ff_a), axis=0).astype('float32'))
                fv.save_index(index_file)
                self.tenant_feature_vectors[ta] = fv

        logger.info(f"global feature init vectors success.")

    def add_face_list(self):
        pass

    def add_face(self, tenant_id, face_id, feature_vector):
        if tenant_id not in self.tenant_feature_vectors:
            logger.info(f"global feature vector pool not {tenant_id} feature index object.")
            fdb_name = f"{tenant_id}.db"
            index_file = os.path.join(FEATURE_DB_DIR, fdb_name)
            self.tenant_feature_vectors[tenant_id] = FaceVectorIndex(index_file=index_file)

        fv = self.tenant_feature_vectors[tenant_id]
        fv.add_face_vector(user_id=int(face_id),
                           face_vector=np.expand_dims(np.array(feature_vector), axis=0).astype("float32"))

        if FEATURE_DB_REAL_TIME_UPDATE:
            fv.save_index()

    def delete_face(self, tenant_id, face_id: List):
        if tenant_id in self.tenant_feature_vectors:
            fv = self.tenant_feature_vectors[tenant_id]
            fv.remove_face_vector(user_id=face_id)
            if FEATURE_DB_REAL_TIME_UPDATE:
                fv.save_index()
        else:
            logger.error(
                f"delete face index error:because global feature vector pool not {tenant_id} feature index object.")

    def update_face(self, tenant_id, face_id, new_feature_vector):
        if tenant_id in self.tenant_feature_vectors:
            fv = self.tenant_feature_vectors[tenant_id]
            fv.update_face_vector(user_id=int(face_id),
                                  new_face_vector=np.expand_dims(np.array(new_feature_vector), axis=0).astype(
                                      "float32"))
            if FEATURE_DB_REAL_TIME_UPDATE:
                fv.save_index()
            logger.info(f"{tenant_id} update face feature index success in global feature vector pool")
        else:
            logger.error(
                f"update face index error:because global feature vector pool not {tenant_id} feature index object.")

    def search_face(self, tenant_id, feature_vector, top_k=5):
        if tenant_id in self.tenant_feature_vectors:
            fv = self.tenant_feature_vectors[tenant_id]
            D, I = fv.search_face_vector(
                query_vector=np.expand_dims(np.array(feature_vector), axis=0).astype("float32"),
                k=top_k)  #
            return D, I
        else:
            logger.error(
                f"search face index error:because global feature vector pool not {tenant_id} feature index object.")
            msg = FaceRecStatusParameter.face_feature_vector_db_not_exist.info()
            code = FaceRecStatusParameter.face_feature_vector_db_not_exist.code()
            raise NormalErrorException(msg, code)
