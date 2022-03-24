import cv2
import matplotlib.pyplot as plt
import numpy as np


def visualize(y, isPlot=True):
    x = list(range(len(y)))
    fig, ax = plt.subplots()
    if isPlot:
        ax.plot(x, y)
    else:
        ax.scatter(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("values")

    plt.show()


"""vis_labels(dataHodler) or vis_labels(values=values, labels=labels)"""
def vis_labels(hodler=None, values=[], labels=[]):
    # circular import otherwise
    from prod.kmglift_api import LiftData, Label

    if type(hodler) == LiftData:
        values = hodler.liftDataSec._values
        labels = hodler.liftDataSec._labels

    # [[NODATA], [UP], [DOWN], [OTHER-STAG]]
    x, y = [[], [], [], [], []], [[], [], [], [], []]

    for i in range(len(values)):
        id = int(labels[i].value)
        x[id].append(i)
        y[id].append(values[i])

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    #orig
    ax[0].plot(list(range(len(values))), values)

    ax[1].scatter(x[0], y[0], label=Label.NODATA.name, c="b")
    ax[1].scatter(x[1], y[1], label=Label.DOWN.name, c="g")
    ax[1].scatter(x[2], y[2], label=Label.UP.name, c="r")
    ax[1].scatter(x[3], y[3], label=Label.OTHER.name, c="y")
    ax[1].scatter(x[4], y[4], label=Label.ANOMALY.name, c="m")

    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")

    plt.show()


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
def resize_plotMat(plotMat, width, height):
    if len(plotMat[0]) < width:
        print("check resize_plotMat")

    window = round(len(plotMat[0]) / width)
    mat = squeeze(plotMat, window) if window > 1 else plotMat

    # Возможны искажения при горизонтальных линиях
    return cv2.resize(mat, (len(mat[0]), height))


""" Возвращает изображение 720px высотой и примерно 1280px шириной """
def imshow(title, img, width=1280, height=720):
    cv2.imshow(title, resize_plotMat(img, width, height))
