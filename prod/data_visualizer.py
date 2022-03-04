import matplotlib.pyplot as plt
import matplotlib


def visualize(y):
    x = list(range(len(y)))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("time")
    ax.set_ylabel("values")


"""
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER-STAG = 3
"""
def vis_labels(values, labels):
    # [[NODATA], [UP], [DOWN], [OTHER-STAG]]
    x, y = [[],[],[],[]], [[],[],[],[]]

    for i in range(len(values)):
        id = int(labels[i])
        x[id].append(i)
        y[id].append(values[i])

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    #orig
    ax[0].plot(list(range(len(values))), values)

    ax[1].scatter(x[0], y[0], label="NODATA", c="blue")
    ax[1].scatter(x[1], y[1], label="DOWN", c="green")
    ax[1].scatter(x[2], y[2], label="UP", c="red")
    ax[1].scatter(x[3], y[3], label="OTHER-STAG", c="yellow")

    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")

    plt.show()