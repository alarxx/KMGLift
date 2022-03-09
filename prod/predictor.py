import numpy as np

from prod.data_io import loadLiftDataSec
from prod.data_visualizer import vis_labels
from prod.data_wrapper import LiftDataSec, LiftOpsPeriods
from prod.labels import Label
from prod.visual_filter import visual_filter


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
    periods = LiftOpsPeriods(filtered)

    for i in range(len(periods)):
        s = periods.start(i)
        e = periods.end(i)
        label = by_apr(filtered[s:e])

        liftData._labels[s:e] = [label] * (e-s)

        periods._labels[i] = label

    return periods


def test_predictor():
    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name
    liftData = loadLiftDataSec(dir)
    predict_labels(liftData)
    vis_labels(liftData)


def test_oper_time():
    arr = [1, 1, 1, 1, 1,
           0,
           1, 1, 1,
           0,
           1]
    periods = LiftOpsPeriods(arr)
    print(len(arr), periods)

    arr = [0,
           1, 1, 1, 1, 1,
           0,
           1, 2, 3,
           0,
           1,
           0]
    periods = LiftOpsPeriods(arr)
    print(len(arr), periods)


def test_apr_labels():
    arr = [0, 1, 2, 3, 0, 3, 2, 1, 0, 1, 1, 1]
    liftData = LiftDataSec()
    for i, val in enumerate(arr):
        liftData.add(i, val)

    print("liftDataPrev: \n", liftData)

    periods = LiftOpsPeriods(liftData._values)
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

