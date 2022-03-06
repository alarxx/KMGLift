import openpyxl
from data_visualizer import vis_labels
from prod.data_wrapper import DataHodler
from prod.time_converter import hms2sec


"""Returns values and labels"""
def stretch_by_seconds(xlsx_dir, dataHodler=DataHodler(), day=0):
    book = openpyxl.open(xlsx_dir, read_only=True)
    sheet = book.active

    daySec = day*86400

    for xlsx_strHMS, xlsx_val, xlsx_dur in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=0, max_col=3):
        if not (isinstance(xlsx_val.value, float) or isinstance(xlsx_val.value, int)):
            continue

        timeInSec = hms2sec(xlsx_strHMS.value)
        duration = hms2sec(xlsx_dur.value)

        for s in range(timeInSec, timeInSec+duration):
            dataHodler.add(daySec + s, xlsx_val.value)

    return dataHodler


if __name__ == "__main__":

    file_name = "weight_10.06.xlsx"
    dir = "..\\assets\\KMG\\AKSH-283\\" + file_name

    dataHodler = stretch_by_seconds(dir)
    vis_labels(dataHodler._values, dataHodler._labels)

