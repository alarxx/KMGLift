from prod.labels import Label

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

    def add(self, id, value, label=Label.OTHER):
        miss = (id-len(self))
        # if(miss > 0):
        #     print(id)
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
    period - время операции, промежуток от первого ненулевого значения до нулевого значения
    Примеры: 
        1. list [0 1 2 3 0] -- time [1, 4) 
        2. list [0 1 2 3 4] -- [1, len(list))
    Каждый период имеет label
"""
class LiftOpsPeriods:
    def __init__(self, values):
        self._periods = []
        self.__operations_time(values)

        self._labels = [Label.OTHER] * len(self)

    def __operations_time(self, values):
        # Сложнаватая логика, пересмотреть!
        isClose = True
        start = 0
        for i in range(len(values)):
            if values[i] == 0:
                if not isClose:
                    self._periods.append((start, i))
                isClose = True
            elif isClose:
                isClose = False
                start = i

        if not isClose:
            self._periods.append((start, len(values)))

    def start(self, id):
        return self._periods[id][0]

    def end(self, id):
        return self._periods[id][1]

    def getOp(self, id):
        return self._periods[id], self._labels[id]

    def __len__(self):
        return len(self._periods)

    def __str__(self):
        return "periods: " + str(self._periods) + "\nlabels: " + str(self._labels)


