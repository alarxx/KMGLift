import datetime
import os
from enum import Enum, unique
from pathlib import Path

import numpy as np
import cv2
import openpyxl


""" TIME CONVERTER """


def sec2hms(secArg):
    return str(datetime.timedelta(seconds=secArg))


def hms2sec(strHMS):
    arrHMS = str(strHMS).split(":")
    h, m, s = arrHMS[0], arrHMS[1], arrHMS[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


""" Labels Enum """


""" Label - вид процесса"""
@unique
class Label(Enum):
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER = 3


"""  Data Wrappers """


"""
    Класс отвечает только за хранение данных в секундах.
    За обратную интерпретацию должен отвечать уже другой класс
"""
class LiftDataSec:
    def __init__(self):
        self._values = []
        self._labels = []
        self._maxVal = 0
        # Либо среднее, либо макс в окне, для оптимизации виз фильтра
        # self._compressed = []

    def add(self, sec, value, label=Label.OTHER):
        miss = (sec - len(self))

        self._values.extend([0] * miss + [value])

        self._labels.extend([Label.NODATA] * miss + [label])

        self._maxVal = max(value, self._maxVal)

    def __len__(self):
        return len(self._values)

    def __str__(self):
        return "_values: " + str(self._values) + " - ${_maxVal} = " + str(self._maxVal) + "\n_labels: " + str(self._labels)




""" 
    В периодах пока нет NODATA
    all periods - время обнаруженных операций, промежуток от первого ненулевого значения до нулевого значения
    Примеры: 
        1. list [0 1 2 3 0] -- period [1, 4), Label.UP
        2. list [0 1 2 3 4] -- period [1, len(list)), Label.UP
    Каждый период имеет label
    
    period - объединенные последовательные и одинаковые процессы
"""
class LiftOpsPeriods:
    def __init__(self, values):
        self._allPeriods = self.__operations_time(values)
        self._allLabels = [Label.OTHER] * len(self)

        # self._periods = []
        # self._labels = []

    def __operations_time(self, values):
        periods = []
        # Сложнаватая логика, пересмотреть!
        isClose = True
        start = 0
        for i in range(len(values)):
            if values[i] == 0:
                if not isClose:
                    periods.append([start, i])
                isClose = True
            elif isClose:
                isClose = False
                start = i

        if not isClose:
            periods.append([start, len(values)])

        return periods

    def getAllStartsHMS(self):
        return list(map(lambda x: sec2hms(x[0]), self._allPeriods))

    def getAllEndsHMS(self):
        return list(map(lambda x: sec2hms(x[1]), self._allPeriods))

    def getAllDtsSec(self):
        return list(map(lambda x: (x[1] - x[0]), self._allPeriods))

    def getAllLabelNames(self):
        return list(map(lambda x: x.name, self._allLabels))

    def getStartS(self, id):
        return self._allPeriods[id][0]

    def getEndS(self, id):
        return self._allPeriods[id][1]

    def getDtS(self, id):
        return self.getEndS(id) - self.getStartS(id)

    def getStartHMS(self, id):
        return sec2hms(self.startSec(id))

    def getEndHMS(self, id):
        return sec2hms(self.endSec(id))

    def getDtHMS(self, id):
        return sec2hms(self.endSec(id))

    def getLabel(self, id):
        return self._allLabels[id]

    def __len__(self):
        return len(self._allPeriods)

    def __str__(self):
        return "allPeriods: " + str(self._allPeriods) + "\nallLabels: " + str(self._allLabels)
               # + "\nperiods: " + str(self._periods) + "\nlabels: " + str(self._labels)

    """ 
        Объединение одинаковых последовательных операций в одну 
        Не учитаваются, перескакивает промежутки между оперциями
    """
    # def sameSequence(self):
    #     #На этой стадии нет лейбла OTHER, только UP and DOWN
    #     lastLabel = Label.OTHER
    #     isClosed = True
    #     for i in range(len(self)):
    #         if isClosed:
    #             # Открытие
    #             self._periods.append([self.startS(i), self.endS(i)])
    #             lastLabel = self.label(i)
    #             isClosed = False
    #         else:
    #             # закрытие
    #             if i == (len(self)-1): # Последняя оперция
    #                 self._periods[len(self._periods) - 1][1] = self.endS(i)
    #                 isClosed = True
    #             elif lastLabel != self.label(i+1):
    #                 self._periods[len(self._periods) - 1][1] = self.endS(i)
    #                 isClosed = True
    #
    #             # Добавляем label
    #             if isClosed == True:
    #                 self._labels.append(lastLabel)


""" DATA IO"""


""" 
    Stretches data by seconds.
    Returns holder of (values, labels).
"""
def loadLiftDataSec(xlsx_dir, liftData=LiftDataSec(), day=0):
    book = openpyxl.open(xlsx_dir, read_only=True)
    sheet = book.active

    daySec = day*86400

    for xlsx_strHMS, xlsx_val, xlsx_dur in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=0, max_col=3):
        if not (isinstance(xlsx_val.value, float) or isinstance(xlsx_val.value, int)):
            continue

        timeInSec = hms2sec(xlsx_strHMS.value)
        duration = hms2sec(xlsx_dur.value)

        for s in range(timeInSec, timeInSec+duration):
            liftData.add(daySec + s, xlsx_val.value)

    return


""" VISUAL FILTER """


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


""" PREDICTOR """


def by_apr(y):
    label = Label.OTHER
    # print(len(y))
    # if len(y) < 10:
    #     return label
    # y = np.delete(y, [0, 1, len(y)-2, len(y)-1])

    x = range(len(y))
    z = np.polyfit(x, np.array(y), 1)

    k = z[0]
    # print(k)
    min_grad = 0.0005
    if k > min_grad:
        label = Label.UP
    elif k < -min_grad:
        label = Label.DOWN

    return label


def predict_labels(liftDataSec):
    filtered = visual_filter(liftDataSec)
    # print(filtered)
    periods = LiftOpsPeriods(filtered)

    for i in range(len(periods)):
        s = periods.getStartS(i)
        e = periods.getEndS(i)
        label = by_apr(filtered[s:e])

        liftDataSec._labels[s:e] = [label] * (e - s)

        periods._allLabels[i] = label
    # periods.sameSequence()
    return periods


""" MAIN ABSTRACTION """


class LiftData:

    # @param xlsx_files -- лист файлов
    #  <- процессы могут перетекать изо дня в день -> брать день по названию файла, не совсем правильно, если это лист
    def __init__(self, xlsx_files):
        # base, ext = os.path.splitext(xlsx_files[0])
        # dirpath, filename = os.path.split(base)
        self.date = Path(xlsx_files[0]).stem # Без нескольких расширений файла

        self.liftDataSec = self.__loadData(xlsx_files)
        self.periods = predict_labels(self.liftDataSec)

    def __loadData(self, xlsx_files):
        liftDataSec = LiftDataSec()
        for i in range(len(xlsx_files)):
            loadLiftDataSec(xlsx_files[i], liftDataSec, i)
        return liftDataSec

    # Пока что возвращает все процессы, которые удается найти
    def getData(self):
        p = self.periods
        start = p.getAllStartsHMS()
        end = p.getAllEndsHMS()
        duration = p.getAllDtsSec()
        y = p.getAllLabelNames()

        return {
            'data': {
                'start': start,
                'end': end,
                'duration': duration,
                'y': y
            }
        }
