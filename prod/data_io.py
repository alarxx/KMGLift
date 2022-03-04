import openpyxl
import datetime
import numpy as np
from data_visualizer import vis_labels


def sec2hms(secArg):
    return str(datetime.timedelta(seconds=secArg))


def hms2sec(strHMS):
    arrHMS = str(strHMS).split(":")
    h, m, s = arrHMS[0], arrHMS[1], arrHMS[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


"""Returns values and labels"""
def stretch_by_seconds(xlsx_dir):
    book = openpyxl.open(xlsx_dir, read_only=True)
    sheet = book.active

    res_values = np.zeros(86400) #[]
    res_labels = np.zeros(86400)

    for xlsx_strHMS, xlsx_val, xlsx_dur in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=0, max_col=3):
        if not (isinstance(xlsx_val.value, float) or isinstance(xlsx_val.value, int)):
            continue

        timeInSec = hms2sec(xlsx_strHMS.value)
        duration = hms2sec(xlsx_dur.value)

        for s in range(timeInSec, timeInSec+duration):
            res_values[s] = xlsx_val.value
            res_labels[s] = 3

    return res_values, res_labels


if __name__ == "__main__":

    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    y, l = stretch_by_seconds(dir)
    vis_labels(y, l)

