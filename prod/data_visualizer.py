import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy import uint8


def vis_vector(y, isPlot=True, title="Title", stop=False):
    x = list(range(len(y)))
    fig, ax = plt.subplots()
    if isPlot:
        ax.plot(x, y)
    else:
        ax.scatter(x, y)

    ax.set_title(title)
    ax.set_xlabel("time")
    ax.set_ylabel("values")
    
    if stop:
        plt.show()
        cv2.waitKey(0)
        plt.close()


"""vis_labels(LiftData) or vis_labels(values=values, labels=labels)"""
def vis_labels(liftData=None, values=[], labels=[]):
    # circular import otherwise
    from prod.kmglift_api import LiftData, Label
    from prod.kmglift_api import getPoly, LiftDataSec

    if type(liftData) == LiftData:
        values = liftData.liftDataSec._values
        labels = liftData.liftDataSec._labels
    elif type(liftData) == LiftDataSec:
        values = liftData._values
        labels = liftData._labels

    # vis_vector(values, title="orig")

    # [[NODATA], [UP], [DOWN], [OTHER-STAG]]
    x, y = [[], [], [], [], []], [[], [], [], [], []]

    for i in range(len(values)):
        id = int(labels[i].value)
        x[id].append(i)
        y[id].append(values[i])

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    #orig
    ax[0].plot(list(range(len(values))), values)
    ax[0].set_title("orig")

    ax[1].scatter(x[0], y[0], label=Label.NODATA.name, c="b")
    ax[1].scatter(x[1], y[1], label=Label.DOWN.name, c="g")
    ax[1].scatter(x[2], y[2], label=Label.UP.name, c="r")
    ax[1].scatter(x[3], y[3], label=Label.OTHER.name, c="y")
    ax[1].scatter(x[4], y[4], label=Label.ANOMALY.name, c="m")

    ax[1].set_title("labels")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")


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

    res = np.zeros((rows, cols), dtype=uint8)

    for c in range(cols):
        for r in range(rows):
            a = plotMat[r][c * window: c * window + window]
            for i in range(len(a)):
                if a[i] > 0:
                    res[r][c] = 255
                    break

    return res


""" Возвращает изображение 720px высотой и примерно 1280px шириной """
def resize_plotMat(plotMat, width, height):
    window = round(len(plotMat[0]) / width)
    mat = squeeze(plotMat, window) if window > 1 else plotMat

    # Возможны искажения при горизонтальных линиях
    res = cv2.resize(mat, (len(mat[0]), height))
    if len(plotMat[0]) < width:
        print("check resize_plotMat")
        #print(len(plotMat[0]), len(plotMat), "\n", len(res[0]), len(res))

    return res


""" Возвращает изображение 720px высотой и примерно 1280px шириной """
def imshow(title, img, width=1280, height=720):
    width = 720
    height = 480
    cv2.imshow(title, resize_plotMat(img, width, height))


def draw_poly(values, periods, order):
    vis_vector(getPoly(values, periods, order), title=f"poly{order}")
