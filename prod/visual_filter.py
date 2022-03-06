from prod.data_io import load
from prod.data_visualizer import vis_labels
import numpy as np


"""
    Возвращает матрицу в виде плота
    @param height -- Можем указать любую высоту матрицы - Зависит от максимальной массы.
    Высота пока не важна так как нам не нужно обратное преобразование,
    а нужно только начало и конец операции
"""
def vec2plotMat(vals_vector, height=300):
    # можем указать любую яркость
    px_brightness = 255

    rows = height
    cols = len(vals_vector)

    mat = np.zeros((rows, cols))

    for col in range(cols):
        row = rows - round(vals_vector[col]) - 1
        mat[row][col] = px_brightness
        # Должны нарисовать линию от этой точки до следующей
        if col == cols - 1:
            break
        row1 = rows - round(vals_vector[col + 1]) - 1
        fromm = min(row, row1)
        too = max(row, row1)
        for i in range(fromm, too + 1):
            mat[i][col] = px_brightness

    return mat


def plotMat2vec(plotMat):
    rows = len(plotMat)
    cols = len(plotMat[0])

    vec = np.zeros((cols))

    for c in range(cols):
        for r in range(rows):
            if plotMat[r][c] > 0:
                vec[c] = (rows - r - 1)
                break
    return vec


def visual_filter(vals_vector):
    plotMat = vec2plotMat(vals_vector)
    filtered = plotMat2vec(plotMat)
    return filtered


if __name__ == "__main__":
    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    dataHodler = load(dir)
    filtered = visual_filter(dataHodler._values)

    print(filtered)

    vis_labels(values=filtered, labels=dataHodler._labels)
