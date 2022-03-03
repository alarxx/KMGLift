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

    isFirstTime = True
    old_time = 0

    time_res = []
    result = []

    for strHMS, val in sheet.iter_rows(min_row=0, max_row=sheet.max_row, min_col=0, max_col=2):
        if not isinstance(val.value, float):
            continue

        total_seconds = hms2sec(strHMS.value)

        # Записываем от начала записи времени, а не от нуля
        if isFirstTime:
            old_time = total_seconds
            isFirstTime = False

        for s in range(old_time, total_seconds):
            time_res.append(s)
            result.append(val.value)

        old_time = total_seconds

    return  np.asarray(time_res), np.asarray(result)


if __name__ == "__main__":
    file_name = "weight_01.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    t, y = time_step(dir)

    print(y)
    print(t)

    x = list(range(len(y)))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("value")
    plt.show()
