import matplotlib.pyplot as plt

from prod_test.data_wrapper import LiftDataSec
from prod_test.labels import Label


def visualize(y):
    x = list(range(len(y)))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("values")


"""vis_labels(dataHodler) or vis_labels(values=values, labels=labels)"""
def vis_labels(hodler=None, values=[], labels=[]):
    if len(values) == 0 and len(labels) == 0:
        if type(hodler) == LiftDataSec:
            values = hodler._values
            labels = hodler._allLabels
        else: # type(liftData) == LiftData
            values = hodler.liftDataSec._values
            labels = hodler.liftDataSec._labels

    # [[NODATA], [UP], [DOWN], [OTHER-STAG]]
    x, y = [[], [], [], []], [[], [], [], []]

    for i in range(len(values)):
        id = int(labels[i].value)
        x[id].append(i)
        y[id].append(values[i])

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    #orig
    ax[0].plot(list(range(len(values))), values)

    ax[1].scatter(x[0], y[0], label=Label.NODATA.name, c="blue")
    ax[1].scatter(x[1], y[1], label=Label.DOWN.name, c="green")
    ax[1].scatter(x[2], y[2], label=Label.UP.name, c="red")
    ax[1].scatter(x[3], y[3], label=Label.OTHER.name, c="yellow")

    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")

    plt.show()


def print_periods(liftData):
    for i in range(len(liftData.periods)):
        s, e, l, dt = liftData.periods.time_label_dt(i)
        print("time --", s + "-" + e, "; label --", l, "; duration --", dt)