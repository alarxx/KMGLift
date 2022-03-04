import numpy as np


class DataHodler:
    def __init__(self):
        self._values = np.zeros(86400)
        self._labels = np.zeros(86400)
        self._maxVal = 0

    def set(self, id, value, label):
        self._values[id] = value
        self._labels[id] = label
        self._maxVal = max(value, self._maxVal)

    def get(self, id):
        return self._values[id], self._labels[id]


if __name__ == "__main__":
    dataHodler = DataHodler()
    v, l = dataHodler.get(0)
    print(dataHodler._values)