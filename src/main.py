import data_io
from visual_filter import visual_filter
from labels import predict_labels, scale_labels, operations, label
from prod.data_visualizer import vis_labels
import matplotlib.pyplot as plt
import datetime


def time2sec(t):
    t = str(t).split(":")
    h, m, s = t[0], t[1], t[2]
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())

def difference(t1, t2):
    s = time2sec(t2) - time2sec(t1)
    return str(datetime.timedelta(seconds=s))


if __name__ == "__main__":
    file_name = "\\AKSH-283\\weight_03.06.xlsx"
    dir = "..\\assets\\KMG" + file_name

    orig, time1 = data_io.time_step(dir)

    window = 17
    filtered = visual_filter(orig, window=window, max_val=255)
    scaled_labels = predict_labels(filtered)
    labels = scale_labels(orig, scaled_labels, window)

    # operations [[start, end]]
    ids = operations(labels)
    for i in range(len(ids)):
        dt = difference(time1[ids[i][0]], time1[ids[i][1]])
        print(i, ":", label(labels[ids[i][0]]), ";", time1[ids[i][0]], "-", time1[ids[i][1]], ";", 
                "duration =", dt)

    # mse_draw(filtered)
    # vis_labels(filtered, scaled_labels)
    vis_labels(orig, labels)
    print("Для остановки: Ctrl + C")
    plt.show()