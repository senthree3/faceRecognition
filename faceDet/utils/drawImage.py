# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/12/12 15:06
"""
import cv2


def draw_focus_bbox(image, bbox, is_original_draw=False, is_focus_object=False, text=None):
    """
    在图像上绘制矩形框并添加文字。

    参数：
    - image: 输入的原始图像
    - bbox: 矩形框的坐标，格式为 (x_min, y_min, x_max, y_max)
    - is_focus_object: 是否为重点对象，如果是，矩形框为红色，否则为绿色
    - text: 要添加的文字内容，如果为None，则不添加文字

    返回值：
    - result_image: 处理后的图像
    """

    # 复制原始图像，以防止修改原始图像
    if is_original_draw:
        result_image = image
    else:
        result_image = image.copy()

    # 提取矩形框坐标
    x_min, y_min, x_max, y_max = map(int, bbox)

    # 设置矩形框颜色
    bbox_color = (0, 255, 0)  # 默认为绿色
    if is_focus_object:
        bbox_color = (0, 0, 255)  # 如果是重点对象，设置为红色

    # 在图像上绘制矩形框
    cv2.rectangle(result_image, (x_min, y_min), (x_max, y_max), bbox_color, 2)

    # 添加文字
    if text is not None:
        # 设置文字的位置为矩形框左上角
        text_position = (x_min, y_min - 10)
        # 设置文字颜色和字体
        text_color = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1

        # 在图像上添加文字
        cv2.putText(result_image, text, text_position, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    return result_image


class DrawBBox(object):
    def __init__(self, image, is_original_draw=False):
        self.image = image
        self.bbox_color = (0, 255, 0)
        self.thickness = 2
        self.copy_image = self.image if is_original_draw else self.image.copy()

    def draw_one_bbox(self, bbox, bbox_color=None, thickness=None, text=None, text_color=None):
        result_image = self.copy_image
        if bbox_color is None:
            bbox_color = self.bbox_color
        if thickness is None:
            thickness = self.thickness

        x_min, y_min, x_max, y_max = map(int, bbox)
        cv2.rectangle(result_image, (x_min, y_min), (x_max, y_max), bbox_color, thickness=thickness)

        if text is not None:
            # 设置文字的位置为矩形框左上角
            text_position = (x_min, y_min - 10)
            # 设置文字颜色和字体
            if text is None:
                text_color = self.bbox_color
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1

            # 在图像上添加文字
            cv2.putText(result_image, text, text_position, font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        return result_image

    def draw_bbox_list(self, bbox_list, bbox_color=None, thickness=None, text=None, text_color=None):
        result_image = self.copy_image
        for bbox in bbox_list:
            result_image = self.draw_one_bbox(bbox, bbox_color, thickness, text, text_color)
        return result_image
