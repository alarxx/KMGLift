import numpy as np
import cv2


"""
    !В удобный для изображений 32-битный диапазон [0; 255]
    !высота изображения после toPlotImage будет равна 256
    Хм... возможно число 255 взято рандомно, можно взять и 1000
"""


def my_range(orig, max_val=255):
    maxx = np.amax(orig)
    arr = np.zeros((len(orig)))
    for i in range(len(orig)):
        val = orig[i]
        if(orig[i] < 1):
            val = 0
        arr[i] = int(round(max_val * ( val / maxx)))
    return arr.astype(int)


"""
    Вектор с данными в изображение-график с линиями
"""


def toPlotImage(y, max_val):
    # Да val равен max_val, но мы можем указать любую яркость
    pixel_brightness = 255
    rows = max_val + 1
    cols = len(y)
    mat = np.zeros((rows, cols))
    for col in range(cols):
        row = rows - y[col] - 1
        mat[row][col] = pixel_brightness
        if col == cols - 1:
            break
        row1 = rows - y[col + 1] - 1
        fromm = min(row, row1)
        too = max(row, row1)
        for i in range(fromm, too + 1):
            mat[i][col] = pixel_brightness
    return mat


def toVec(mat):
    rows = len(mat)
    cols = len(mat[0])

    arr = np.zeros((cols))

    for c in range(cols):
        for r in range(rows):
            if mat[r][c] > 0:
                arr[c] = (rows - r - 1)
                break



    return arr


""" 
    Сужает по горизонтали 
    -> 1 0 0 <-         1
    -> 0 1 0 <-    =    1
    -> 0 0 0 <-         0

    y = [1 2 3 0 0 0 3 2 1]

    toPlotImage
    [[0. 1. 1. 0. 0. 1. 1. 0. 0.]
     [1. 1. 1. 0. 0. 1. 1. 1. 0.]
     [1. 0. 1. 0. 0. 1. 0. 1. 1.]
     [0. 0. 1. 1. 1. 1. 0. 0. 0.]]

    squeeze
    [[1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 0.]]

"""


def squeeze(x, window, val):
    cols = len(x[0]) // window
    if len(x[0]) % window > 0:
        cols += 1
    rows = len(x)

    res = np.zeros((rows, cols))

    for c in range(cols):
        for r in range(rows):
            a = x[r][c * window:c * window + window]
            for i in range(len(a)):
                if a[i] > 0:
                    res[r][c] = val
                    break

    return res


def visual_filter(orig, window, max_val):
    # Да, max_val равен 255, но мы можем указать любую высоту,
    # просто в нашем случае максимальное значение в данных - 25,
    # 255 - с запасом
    y = my_range(orig, max_val=max_val)

    # Вектор с данными в изображение-график с линиями
    mat = toPlotImage(y, max_val=max_val)

    # Кажется, не обязателен, можно добиться того же результата увеличив окно в заполнении фигуры
    # Сжимаем по горизонтали
    mat = squeeze(mat, window=window, val=255)
    # cv2.imshow("orig", mat)

    # Убираем горизонтальные линии типа ---
    kernel = np.ones((13, 1), np.uint8)
    img = cv2.morphologyEx(mat, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("lines", img)

    # Почему бы не избавить от выбросов в данных

    # Заполняем фигуру
    kernel = np.ones((1, 3), np.uint8)
    img2 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("fill", img2)

    # Фильтруем шум - выбросы
    kernel = np.ones((1, 11), np.uint8)
    filtered = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("filtered", filtered)
    # cv2.waitKey(0)

    return toVec(filtered)
