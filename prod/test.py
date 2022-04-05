import cv2
import numpy as np
from matplotlib import pyplot as plt

from prod.data_visualizer import vis_labels, imshow, resize_plotMat, squeeze
from prod.kmglift_api import vec2mat, mat2vec, Label, LiftDataPeriods, sameSequence, hms2sec, loadDataSec
from prod.lol import Canny


""" 
    Зануляем колебания в u*100kg (горизонтальные линии) 
    --_-_- => 0 
"""
def remove_other(values):
    plotMat = vec2mat(values, isPlot=True)
    kernel = np.ones((7, 10), np.uint8)  # u*100kg
    lines = cv2.morphologyEx(plotMat, cv2.MORPH_OPEN, kernel)
    return mat2vec(lines)


""" Склеить без учета нулевых значений """
def skip_zeros(values):
    pass


def visual_filter(values):
    plotMat = vec2mat(values, isPlot=True)
    # Убираем горизонтальные линии типа ---
    kernel = np.ones((7, 1), np.uint8)  # value*100kg
    lines = cv2.morphologyEx(plotMat, cv2.MORPH_OPEN, kernel)
    imshow("lines", lines)

    # gray = cv2.cvtColor(lines, cv2.COLOR_BGR2GRAY)
    """ Данные сжимаются в 60 раз """
    src = squeeze(lines, 1*60)
    # print(src.shape)
    filtered = mat2vec(src)
    src = vec2mat(filtered, isPlot=False)

    imshow("src", resize_plotMat(src, 720, 480))
    cv2.waitKey(0)


def main():
    dir = "..\\assets\\KMG\\AKSH-283\\"
    xlsx_file = dir + "weight_12.06.xlsx"

    liftDataSec = loadDataSec(xlsx_file)

    visual_filter(liftDataSec._values)


if __name__ == "__main__":
    # arr = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 0.3, 0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 1, 2, 3]
    # print(arr)
    # mat = vec2mat(arr, isPlot=True)
    # print(mat)
    # vec = mat2vec(mat)
    # print(vec)

    main()