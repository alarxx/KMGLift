from prod.labels import Label
from prod.time_converter import sec2hms

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


if __name__ == "__main__":
    liftData = LiftDataSec()
    liftData.add(5, 5)
    liftData.add(6, 5)
    liftData.add(7, 7)
    liftData.add(8, 5)
    print(liftData)


""" 
    В периодах пока нет NODATA
    period - время операции, промежуток от первого ненулевого значения до нулевого значения
    Примеры: 
        1. list [0 1 2 3 0] -- period [1, 4), Label.UP
        2. list [0 1 2 3 4] -- period [1, len(list)), Label.UP
    Каждый период имеет label
"""
class LiftOpsPeriods:
    def __init__(self, values):
        self._allPeriods = self.__operations_time(values)
        self._allLabels = [Label.OTHER] * len(self)

        self._periods = []
        self._labels = []

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

    def startS(self, id):
        return self._allPeriods[id][0]

    def endS(self, id):
        return self._allPeriods[id][1]

    def label(self, id):
        return self._allLabels[id]

    def time_label_dt(self, id):
        startTime = sec2hms(self.startS(id))
        endTime = sec2hms(self.endS(id))
        dt = sec2hms(self.endS(id) - self.startS(id))
        label = self.label(id)
        return startTime, endTime, label, dt

    def __len__(self):
        return len(self._allPeriods)

    def __str__(self):
        return "allPeriods: " + str(self._allPeriods) + "\nallLabels: " + str(self._allLabels) + \
               "\nperiods: " + str(self._periods) + "\nlabels: " + str(self._labels)

    """ 
        Объединение одинаковых последовательных операций в одну 
        Не учитаваются, перескакивает промежутки между оперциями
    """
    def sameSequence(self):
        #На этой стадии нет лейбла OTHER, только UP and DOWN
        lastLabel = Label.OTHER
        isClosed = True
        for i in range(len(self)):
            if isClosed:
                # Открытие
                self._periods.append([self.startS(i), self.endS(i)])
                lastLabel = self.label(i)
                isClosed = False
            else:
                # закрытие
                if i == (len(self)-1): # Последняя оперция
                    self._periods[len(self._periods) - 1][1] = self.endS(i)
                    isClosed = True
                elif lastLabel != self.label(i+1):
                    self._periods[len(self._periods) - 1][1] = self.endS(i)
                    isClosed = True

                # Добавляем label
                if isClosed == True:
                    self._labels.append(lastLabel)