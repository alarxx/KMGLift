from prod.data_io import loadLiftDataSec
from prod.data_visualizer import vis_labels, print_periods
from prod.data_wrapper import LiftDataSec
from prod.predictor import predict_labels
from prod.time_converter import sec2hms


class LiftData:
    def __init__(self, xlsx_files):
        self.liftDataSec = self.__loadData(xlsx_files)
        self.periods = predict_labels(self.liftDataSec)

    def __loadData(self, xlsx_files):
        liftDataSec = LiftDataSec()
        for i in range(len(xlsx_files)):
            loadLiftDataSec(xlsx_files[i], liftDataSec, i)
        return liftDataSec


def labelsBySeconds(liftData):
    res = []

    for s in range(len(liftData.liftDataSec)):

        res.append(
                sec2hms(s) + " " +
                liftData.liftDataSec._labels[s].name
        )

    return res


if __name__ == "__main__":
    dir = "..\\assets\\KMG\\AKSH-283\\"

    f1 = dir + "weight_09.06.xlsx"
    f2 = dir + "weight_10.06.xlsx"

    liftData = LiftData([f2])

    # print(liftData.liftDataSec)
    # print(liftData.periods)
    #
    # print_periods(liftData)
    # vis_labels(liftData)

    print(labelsBySeconds(liftData))