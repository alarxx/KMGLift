import openpyxl
import datetime
import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
    

def sec2hms(secArg):
    return str(datetime.timedelta(seconds=secArg))


def hms2sec(strHMS):
    arrHMS = str(strHMS).split(":")
    h, m, s = arrHMS[0], arrHMS[1], arrHMS[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


def time_step(xlsx_dir):
    book = openpyxl.open(xlsx_dir, read_only=True)
    sheet = book.active

    res_values = np.empty(86400) #[]
    res_labels = np.empty(86400)

    for xlsx_strHMS, xlsx_val, xlsx_dur in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=0, max_col=3):
        if not (isinstance(xlsx_val.value, float) or isinstance(xlsx_val.value, int)):
            continue

        timeInSec = hms2sec(xlsx_strHMS.value)
        duration = hms2sec(xlsx_dur.value)

        for s in range(timeInSec, timeInSec+duration):
            res_values[s] = xlsx_val.value
            res_labels[s] = 3

    return res_values, res_labels


"""
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER-STAG = 3
"""
def vis_labels(values, labels):
    # [[NODATA], [UP], [DOWN], [OTHER-STAG]]
    x, y = [[],[],[],[]], [[],[],[],[]]

    for i in range(len(values)):
        id = int(labels[i])
        x[id].append(i)
        y[id].append(values[i])

    fig, ax = plt.subplots(1, 2, figsize=(15,5))

    #orig
    ax[0].plot(list(range(len(values))), values)

    ax[1].scatter(x[0], y[0], label="NODATA", c="blue")
    ax[1].scatter(x[1], y[1], label="DOWN", c="green")
    ax[1].scatter(x[2], y[2], label="UP", c="red")
    ax[1].scatter(x[3], y[3], label="OTHER-STAG", c="yellow")

    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")

    plt.show()



if __name__ == "__main__":

    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    y, l = time_step(dir)

    vis_labels(y, l)

