# coding=utf-8
import win32api, win32con
import win32gui
import win32print
import numpy as np
import cv2


def getScreenRes():
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, win32con.HORZRES)
    height = win32print.GetDeviceCaps(hDC, win32con.VERTRES)
    return width, height


def getScreenRes2():
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    return width, height


def getScreenSize():
    hDC = win32gui.GetDC(0)
    width_mm = win32print.GetDeviceCaps(hDC, win32con.HORZSIZE)
    height_mm = win32print.GetDeviceCaps(hDC, win32con.VERTSIZE)
    return width_mm, height_mm


def getScreenPPM():
    width, height = getScreenRes()
    width_mm, height_mm = getScreenSize()
    ppm_w = width * 1.0 / width_mm
    ppm_h = height * 1.0 / height_mm
    return ppm_w, ppm_h


def genRuler(length_cm=20, width_pixel=120):
    """
    尺子绘制函数

    :param length_cm: 尺子长度，单位厘米，默认20cm
    :param width_pixel: 尺子宽度，单位毫米，默认120mm
    :return:
    """

    # 配色方案
    color_style = []
    color_style.append((255, 255, 255))  # 文字、刻线颜色
    color_style.append([204, 144, 94])  # 浅背景色
    color_style.append([172, 93, 0])  # 深背景色

    # 获取屏幕基础信息
    ppm, _ = getScreenPPM()
    total_length_mm = length_cm * 10
    total_length_pixel = int(ppm * total_length_mm)

    # 背景绘制
    background = np.zeros([width_pixel, total_length_pixel, 3], np.uint8)
    background[:, :, :] = color_style[1]
    background[70:, :, :] = color_style[2]

    # 图案绘制
    cv2.circle(background, (total_length_pixel * 3 / 8, width_pixel - 35), 8, (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(background, (total_length_pixel * 5 / 8, width_pixel - 35), 8, (255, 255, 255), -1, cv2.LINE_AA)
    cv2.line(background,
             (total_length_pixel * 4 / 8 - 10, width_pixel - 12),
             (total_length_pixel * 4 / 8, width_pixel - 7), (255, 255, 255), 3, cv2.LINE_AA)
    cv2.line(background,
             (total_length_pixel * 4 / 8, width_pixel - 7),
             (total_length_pixel * 4 / 8 + 10, width_pixel - 12), (255, 255, 255), 3, cv2.LINE_AA)

    # 文字信息绘制
    cv2.putText(background, "Unit:cm", (5, width_pixel - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                color_style[0], 1,
                cv2.LINE_AA)
    cv2.putText(background, "Zhao Xuhui", (total_length_pixel - 80, width_pixel - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                color_style[0], 1,
                cv2.LINE_AA)

    # 绘制刻线及标注
    for i in range(int(total_length_pixel / ppm) + 1):
        graduation = int(round(i * ppm, 0))
        if i % 10 == 0:  # 整厘米刻线最长
            background[30:70, graduation, :] = color_style[0]
            if i == 0:  # 0标注为了美观稍微移动位置
                cv2.putText(background, (i / 10).__str__(), (graduation + 1, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            color_style[0], 1,
                            cv2.LINE_AA)
            else:
                if i >= 100:  # 两位数标为了美观注稍微移动
                    cv2.putText(background, (i / 10).__str__(), (graduation - 10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color_style[0], 1,
                                cv2.LINE_AA)
                else:
                    cv2.putText(background, (i / 10).__str__(), (graduation - 5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color_style[0], 1,
                                cv2.LINE_AA)
        elif i % 5 == 0:  # .5厘米刻线长一些
            background[40:70, graduation, :] = color_style[0]
        else:  # 其它毫米刻线最短
            background[53:70, graduation, :] = color_style[0]
    return background


def genAreaRuler(length_cm=5, width_cm=5):
    # 颜色样式
    color_style = []
    color_style.append((255, 255, 255))  # 刻线颜色
    color_style.append([204, 144, 94])  # 浅背景色
    color_style.append([172, 93, 0])  # 深背景色
    color_style.append((0, 255, 255))  # 文字颜色

    # 获得屏幕基本信息
    ppm_w, ppm_h = getScreenPPM()
    total_length_mm = length_cm * 10
    total_length_pixel = int(ppm_w * total_length_mm)
    total_width_mm = width_cm * 10
    total_width_pixel = int(ppm_h * total_width_mm)

    # 背景绘制
    background = np.zeros([total_width_pixel, total_length_pixel, 3], np.uint8)
    background[:, :, :] = color_style[2]

    # 虚线绘制
    step_length = 5
    line_color = (255, 255, 255)
    for i in range(int(total_length_pixel / ppm_w) + 1):
        graduation = int(round(i * ppm_w, 0))
        if i % 10 == 0 and i >= 10:
            for i in range(int(total_width_pixel / step_length)):
                if i % 2 == 0:
                    cv2.line(background, (graduation, i * step_length), (graduation, (i + 1) * step_length), line_color)
    for i in range(int(total_width_pixel / ppm_h) + 1):
        graduation = int(round(i * ppm_h, 0))
        if i % 10 == 0 and i >= 10:
            for i in range(int(total_length_pixel / step_length)):
                if i % 2 == 0:
                    cv2.line(background, (i * step_length, graduation), ((i + 1) * step_length, graduation), line_color)

    # 刻线绘制
    for i in range(int(total_length_pixel / ppm_w) + 1):
        graduation = int(round(i * ppm_w, 0))
        if i % 10 == 0:
            background[:40, graduation, :] = color_style[0]
            if i == 0:
                pass
            else:
                if i >= 100:
                    cv2.putText(background, (i / 10).__str__(), (graduation - 10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color_style[3], 1,
                                cv2.LINE_AA)
                else:
                    cv2.putText(background, (i / 10).__str__(), (graduation - 5, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color_style[3], 1,
                                cv2.LINE_AA)
        elif i % 5 == 0:
            background[:30, graduation, :] = color_style[0]
        else:
            background[:17, graduation, :] = color_style[0]
    for i in range(int(total_width_pixel / ppm_h) + 1):
        graduation = int(round(i * ppm_h, 0))
        if i % 10 == 0:
            background[graduation, :40, :] = color_style[0]
            if i == 0 or i == 10:
                pass
            else:
                cv2.putText(background, (i / 10).__str__(), (45, graduation + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            color_style[3], 1,
                            cv2.LINE_AA)
        elif i % 5 == 0:
            background[graduation, :30, :] = color_style[0]
        else:
            background[graduation, :17, :] = color_style[0]

    # 文字信息绘制
    cv2.putText(background, "Unit:cm", (total_length_pixel - 80, total_width_pixel - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                color_style[0], 1,
                cv2.LINE_AA)
    cv2.putText(background, "Zhao Xuhui", (total_length_pixel - 80, total_width_pixel - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                color_style[0], 1,
                cv2.LINE_AA)
    return background


if __name__ == '__main__':
    area = genAreaRuler(length_cm=10, width_cm=6)
    cv2.imwrite("areaRuler.png", area)
    length = genRuler(length_cm=10)
    cv2.imwrite("lengthRuler.png", length)
