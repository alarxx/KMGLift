from prod.data_io import loadLiftDataSec
from prod.data_visualizer import vis_labels
from prod.data_wrapper import LiftDataSec
from prod.predictor import predict_labels


def predict(xlsx_files):
    liftData = LiftDataSec()

    for i in range(len(xlsx_files)):
        loadLiftDataSec(xlsx_files[i], liftData, i)

    periods = predict_labels(liftData)

    return liftData, periods


if __name__ == "__main__":
    dir = "..\\assets\\KMG\\AKSH-283\\"

    f1 = dir + "weight_09.06.xlsx"
    f2 = dir + "weight_10.06.xlsx"

    liftDataSec, periods = predict([f2])

    print(periods)
    vis_labels(liftDataSec)