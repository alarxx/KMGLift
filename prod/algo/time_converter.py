import datetime


def sec2hms(secArg):
    return str(datetime.timedelta(seconds=secArg))


def hms2sec(strHMS):
    arrHMS = str(strHMS).split(":")
    h, m, s = arrHMS[0], arrHMS[1], arrHMS[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
