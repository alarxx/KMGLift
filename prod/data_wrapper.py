from prod.labels import Label

"""
    Класс отвечает только за хранение данных в секундах.
    За обратную интерпретацию должен отвечать уже другой класс
"""
class DataHodler:
    def __init__(self):
        self._values = []
        self._labels = []
        self._maxVal = 0
        # Либо среднее, либо макс в окне
        # self._compressed = []

    def add(self, id, value, label=Label.OTHER):
        miss = (id-len(self))
        self._values.extend([0] * miss + [value])

        self._labels.extend([Label.NODATA] * miss + [label])

        self._maxVal = max(value, self._maxVal)

    def get(self, id):
        return self._values[id], self._labels[id]

    def setLabel(self, id, label):
        self._labels[id] = label

    def __len__(self):
        return len(self._values)

    def __str__(self):
        return "_values: " + str(self._values) + " - ${_maxVal} = " + str(self._maxVal) + "\n_labels: " + str(self._labels)


if __name__ == "__main__":
    dataHodler = DataHodler()
    dataHodler.add(5, 5)
    dataHodler.add(6, 5)
    dataHodler.add(7, 7)
    dataHodler.add(8, 5)
    print(dataHodler)