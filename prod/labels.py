"""
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER-STAG = 3
"""


def n2label(n):
    str = "NODATA"
    if n == 1:
        str = "DOWN"
    elif n == 2:
        str = "UP"
    elif n == 3:
        str = "OTHER-STAG"
    return str


def predict_labels(y, l):

    return l