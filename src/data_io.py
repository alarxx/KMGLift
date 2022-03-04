import openpyxl
import datetime
import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
    

def sec2hms(s):
    pass


def hms2sec(strHMS):
    arrHMS = str(strHMS).split(":")
    h, m, s = arrHMS[0], arrHMS[1], arrHMS[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


def time_step(xlsx_dir, step=3):
    book = openpyxl.open(xlsx_dir, read_only=True)

    sheet = book.active

    isFirstTime = True
    old_time = 0
    sec2min = 0  # always less than 60
    mean_value = 0

    result = []
    time_res = []

    for strHMS, val in sheet.iter_rows(min_row=0, max_row=sheet.max_row, min_col=0, max_col=2):
        if not isinstance(val.value, float):
            continue

        total_seconds = hms2sec(strHMS.value)


        # Записываем от начала записи времени, а не от нуля
        if isFirstTime:
            old_time = total_seconds
            isFirstTime = False

        for s in range(old_time, total_seconds):
            sec2min += 1
            mean_value += val.value
            if sec2min == step:
                val_mean = mean_value / step
                result.append(val_mean)

                a = datetime.timedelta(seconds=s)
                time_res.append(str(a))

                sec2min = 0
                mean_value = 0

        old_time = total_seconds

    # print(str(datetime.timedelta(seconds=old_time)))
    return np.asarray(result), np.asarray(time_res)


if __name__ == "__main__":
    file_name = "weight_01.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    step = 1

    y, t = time_step(dir, step)

    print(y)
    print(t)

    x = list(range(len(y)))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("value")

    plt.show()
