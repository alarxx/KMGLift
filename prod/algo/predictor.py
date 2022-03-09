import numpy as np

from prod.algo.data_io import loadLiftData
from prod.algo.data_visualizer import vis_labels
from prod.algo.data_wrapper import LiftData
from prod.labels import Label
from prod.algo.visual_filter import visual_filter

""" 
    Время операции - промежуток от первого ненулевого значения до нулевого значения
    Примеры: 
        list [0 1 2 3 0] -- time [1, 4) 
        list [0 1 2 3 4] -- [1, len(list))
"""
class OperationsTime:
    def __init__(self, values):
        self.operationsTime = self.__operations_time(values)

    def __operations_time(self, values):
        operations = []

        # Сложнаватая логика, пересмотреть!
        isClose = True
        start = 0
        for i in range(len(values)):
            if values[i] == 0:
                if not isClose:
                    operations.append((start, i))
                isClose = True
            elif isClose:
                isClose = False
                start = i

        if not isClose:
            operations.append((start, len(values)))

        return operations

    def start(self, id):
        return self.operationsTime[id][0]

    def end(self, id):
        return self.operationsTime[id][1]

    def __len__(self):
        return len(self.operationsTime)

    def __str__(self):
        return str(self.operationsTime)


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


def predict_labels(liftData):
    filtered = visual_filter(liftData)
    # print(filtered)
    periods = OperationsTime(filtered)

    for i in range(len(periods)):
        s = periods.start(i)
        e = periods.end(i)
        label = by_apr(filtered[s:e])
        liftData._labels[s:e] = [label] * (e-s)


def test_predictor():
    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name
    liftData = loadLiftData(dir)
    predict_labels(liftData)
    vis_labels(liftData)


def test_oper_time():
    arr = [1, 1, 1, 1, 1,
           0,
           1, 1, 1,
           0,
           1]
    periods = OperationsTime(arr)
    print(len(arr), periods)

    arr = [0,
           1, 1, 1, 1, 1,
           0,
           1, 2, 3,
           0,
           1,
           0]
    periods = OperationsTime(arr)
    print(len(arr), periods)


def test_apr_labels():
    arr = [0, 1, 2, 3, 0, 3, 2, 1, 0, 1, 1, 1]
    liftData = LiftData()
    for i, val in enumerate(arr):
        liftData.add(i, val)

    print("liftDataPrev: \n", liftData)

    periods = OperationsTime(liftData._values)
    print("\nperiods: \n", periods, "\n")

    predict_labels(liftData)
    # for i in range(len(periods)):
    #     s = periods.start(i)
    #     e = periods.end(i)
    #     label = by_apr(liftData._values[s:e])
    #     liftData._labels[s:e] = [label] * (e-s)
    print("liftDataResult: \n", liftData)


if __name__ == "__main__":
    # test_predictor()
    # test_oper_time()
    test_apr_labels()

