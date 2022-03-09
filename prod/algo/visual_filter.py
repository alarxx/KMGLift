import cv2
import numpy as np

from prod.algo.data_io import loadLiftData
from prod.algo.data_visualizer import vis_labels


def vec2plotMat(dataHodler):
    # можем указать любую яркость
    px_brightness = 255
    # Значение всегда с десятичной дробью
    rows = int(dataHodler._maxVal * 10)
    cols = len(dataHodler._values)

    mat = np.zeros((rows, cols))

    for col in range(cols):
        # В зависимости от направления роста координат
        row = rows - int(dataHodler._values[col] * 10) - 1
        mat[row][col] = px_brightness

        # Дальше еще должны нарисовать линию от этой точки до следующей

        if col == cols - 1:
            break
        row1 = rows - int(dataHodler._values[col + 1] * 10) - 1
        s = min(row, row1)
        e = max(row, row1)
        for i in range(s, e + 1):
            mat[i][col] = px_brightness

    return mat


def plotMat2vec(plotMat):
    rows = len(plotMat)
    cols = len(plotMat[0])

    vec = np.zeros(cols)
    # Берем самое большое(высокое) значение
    for c in range(cols):
        for r in range(rows):
            if plotMat[r][c] > 0:
                vec[c] = (rows - r - 1) / 10
                break
    return vec


""" 
    Сужает по горизонтали (window = 3)
    -> 1 0 0 <-         1
    -> 0 1 0 <-    =    1
    -> 0 0 0 <-         0
    
    y = [1 2 3 0 0 0 3 2 1]

    toPlotImage
    [[0. 1. 1.  0. 0. 1.  1. 0. 0.]
     [1. 1. 1.  0. 0. 1.  1. 1. 0.]
     [1. 0. 1.  0. 0. 1.  0. 1. 1.]
     [0. 0. 1.  1. 1. 1.  0. 0. 0.]]

    squeeze
    [[1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 0.]]

"""
def squeeze(plotMat, window):
    cols = len(plotMat[0]) // window
    if len(plotMat[0]) % window > 0:
        cols += 1
    rows = len(plotMat)

    res = np.zeros((rows, cols))

    for c in range(cols):
        for r in range(rows):
            a = plotMat[r][c * window: c * window + window]
            for i in range(len(a)):
                if a[i] > 0:
                    res[r][c] = 255
                    break

    return res


""" Возвращает изображение 720px высотой и примерно 1280px шириной """
def resize_plotMat(plotMat):
    # if len(plotMat[0]) < 1280:
    #     return cv2.resize(plotMat, (1280, 720))

    window = round(len(plotMat[0]) / 1280)
    mat = squeeze(plotMat, window) if window > 1 else plotMat
    # Искажения при горизонтальных линиях
    return cv2.resize(mat, (len(mat[0]), 720))
    # return mat


def visual_filter(liftData):
    plotMat = vec2plotMat(liftData)

    # Убираем горизонтальные линии типа ---
    kernel = np.ones((7, 1), np.uint8)
    img = cv2.morphologyEx(plotMat, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("orig", resize_plotMat(plotMat))
    # cv2.imshow("lines", resize_plotMat(img))

    # Заполняем фигуру
    kernel = np.ones((1, 180), np.uint8)
    img2 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("fill", resize_plotMat(img2))

    # Фильтруем шум - выбросы
    kernel = np.ones((1, 90), np.uint8)
    img3 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("filtered", resize_plotMat(img3))
    # cv2.waitKey(0)

    return plotMat2vec(img3)


if __name__ == "__main__":
    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    liftData = loadLiftData(dir)
    filtered = visual_filter(liftData)

    # print(liftData._values[8572], filtered[8572])
    # visualize(liftData._values)
    vis_labels(values=filtered, labels=liftData._labels)
    # vis_labels(values=liftData._values, labels=liftData._labels)
