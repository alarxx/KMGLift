import matplotlib.pyplot as plt
import matplotlib


def visualize(y):
    x = list(range(len(y)))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("1step=3secs")
    ax.set_ylabel("values")


"""
    UP = 0
    DOWN = 1
    STAGNATION = 2
"""
def vis_labels(values, labels):
    # [[UP], [DOWN], [OTHER-STAG]]
    x, y = [[],[],[]], [[], [], []]

    for col in range(len(values)):
        # print(labels[col])
        id = int(labels[col])
        x[id].append(col)
        y[id].append(values[col])

    fig, ax = plt.subplots(1, 2, figsize=(15,5))

    #orig
    ax[0].plot(list(range(len(values))), values)

    ax[1].scatter(x[0], y[0], label="UP", c="red")
    ax[1].scatter(x[1], y[1], label="DOWN", c="green")
    ax[1].scatter(x[2], y[2], label="OTHER", c="yellow")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("values")
    ax[1].legend(loc="best")
    # Деление - примерно 2 часа, можно вывести формулу, но...
    #locator = matplotlib.ticker.LinearLocator(12)
    # Установим локатор для главных меток
    #ax.xaxis.set_major_locator(locator)
    #ax.grid()


    

    #locator = matplotlib.ticker.LinearLocator(12)
    # Установим локатор для главных меток
    #ax.xaxis.set_major_locator(locator)
    #ax.grid()