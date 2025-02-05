# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/10 11:18
"""
import os
import numpy as np
from PIL import Image
from faceDet.libs.scrfd import SCRFD
from faceDet.conf.settings import SCRFD_MODEL_PATH
from faceRec.libs import face_align
from faceRecognition.utils.customException import NormalErrorException
from faceRecognition.enums import FaceRecStatusParameter
from faceRecognition.utils.loggers import logger

detector = SCRFD(SCRFD_MODEL_PATH)
detector.prepare(0)


class ScrfdDetection(object):
    def __init__(self, image, max_num=0):
        """
        :param image: 人脸图像数组数据
        :param max_num: 检测人脸数据量，0为默认所有人脸，1为检测最大像素占用面积人脸
        :return:
        """
        self.max_num = max_num
        self.image = image
        self.bboxes = None
        self.possibility = None
        self.kpss = None
        self.aface = []

    def det(self):
        bboxes1, kpss1 = detector.autodetect(self.image, max_num=self.max_num)
        bboxes = []
        possibility = []
        for row in bboxes1:
            bboxes.append(np.int32(row[:4]).tolist())
            possibility.append(round(np.asscalar(row[-1]), 3))
        if bboxes1.shape[0] == 0:
            msg = FaceRecStatusParameter.zero_face.info()
            code = FaceRecStatusParameter.zero_face.code()
            logger.info(f"{msg}")
            raise NormalErrorException(msg, code)
        self.bboxes = bboxes
        self.possibility = possibility
        self.kpss = kpss1
        return bboxes, possibility, kpss1

    def crop_face(self):
        if self.bboxes is None or self.kpss is None:
            self.det()
        aimg = [face_align.norm_crop(self.image, landmark=kps) for kps in self.kpss]
        self.aface = aimg
        return aimg

    def save_face(self, save_dir):
        if len(self.aface) == 0:
            self.crop_face()
        for idx, f in enumerate(self.aface):
            s_img = Image.fromarray(f)
            os.makedirs(save_dir, exist_ok=True)
            s_img.save(os.path.join(save_dir, f"{idx}.jpg"))


if __name__ == "__main__":
    import cv2
    from faceDet.utils.drawImage import DrawBBox

    _img = "/home/cv/zhouhs/projects/faceRecognition/testData/blm018876.jpg"
    _img = cv2.imread(_img)
    _bboxes, _possibility, _kpss1 = ScrfdDetection(_img).det()
    dbb = DrawBBox(_img)
    _rimg = dbb.draw_bbox_list(_bboxes, bbox_color=(0, 0, 255))
    cv2.imwrite("/home/cv/zhouhs/projects/faceRecognition/testData/out.jpg", _rimg)
