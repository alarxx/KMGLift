"""
    Мысли: 
        В задаче ведь не один день на самом деле, а может быть длина в месяц
        Оперции могут перетекать изо дня в день. 
"""
from prod.labels import Label


class DataHodler:
    def __init__(self):
        #На сколько правильно заранее утверждать длину дня.
        self._values = []
        self._labels = []
        self._maxVal = 0
        # Либо среднее, либо макс в окне
        self._compressed = []

    def add(self, id, value, label=Label.OTHER.value):
        miss = (id-len(self))
        self._values.extend([0] * miss + [value])
        self._labels.extend([0] * miss + [label])

        self._maxVal = max(value, self._maxVal)

    def get(self, id):
        return self._values[id], self._labels[id]

    def __len__(self):
        return len(self._values)

    def __str__(self):
        return "values: " + str(self._values) + "\nlabels: " + str(self._labels)


if __name__ == "__main__":
    dataHodler = DataHodler()
    dataHodler.add(5, 5)
    print(dataHodler)