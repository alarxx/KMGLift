import openpyxl
from data_visualizer import vis_labels
from prod_test.data_wrapper import LiftDataSec
from prod_test.time_converter import hms2sec


""" 
    Stretches data by seconds.
    Returns holder of (values, labels).
"""
def loadLiftDataSec(xlsx_dir, liftData=LiftDataSec(), day=0):
    book = openpyxl.open(xlsx_dir, read_only=True)
    sheet = book.active

    daySec = day*86400

    for xlsx_strHMS, xlsx_val, xlsx_dur in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=0, max_col=3):
        if not (isinstance(xlsx_val.value, float) or isinstance(xlsx_val.value, int)):
            continue

        timeInSec = hms2sec(xlsx_strHMS.value)
        duration = hms2sec(xlsx_dur.value)

        for s in range(timeInSec, timeInSec+duration):
            liftData.add(daySec + s, xlsx_val.value)

    return liftData


if __name__ == "__main__":

    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    liftData = loadLiftDataSec(dir)
    vis_labels(liftData)

