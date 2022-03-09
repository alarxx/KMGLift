from prod.algo.data_io import loadLiftData
from prod.algo.data_visualizer import vis_labels
from prod.algo.data_wrapper import LiftData
from prod.algo.predictor import predict_labels


def predict(xlsx_files):
    liftData = LiftData()

    for i in range(len(xlsx_files)):
        loadLiftData(xlsx_files[i], liftData, i)

    predict_labels(liftData)

    return liftData._values, liftData._labels


if __name__ == "__main__":
    dir = "..\\assets\\KMG\\AKSH-283\\"

    f1 = "weight_09.06.xlsx"
    f2 = "weight_10.06.xlsx"

    values, labels = predict([dir+f1, dir+f2])

    vis_labels(values=values, labels=labels)