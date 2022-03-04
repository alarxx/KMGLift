import numpy as np
from prod import data_visualizer


def by_apr(y):
    label = 2
    # print(len(y))
    if len(y) < 10:
        return label
    y = np.delete(y, [0, 1, len(y)-2, len(y)-1])

    x = range(len(y))
    z = np.polyfit(x, np.array(y), 1)

    k = z[0]
    # print(k)
    min_grad = 0.05
    if k > min_grad:
        label = 0
    elif k < -min_grad:
        label = 1

    return label


def mse_draw(y):
    lin_arr = np.zeros((len(y)))

    isClose = True
    start = 0
    for i in range(len(y)):
        if y[i] == 0:
            if not isClose:
                arr = y[start:i]

                x = list(range(start, i))
                z = np.polyfit(x, np.array(arr), 1)
                p = np.poly1d(z)

                for id in range(start, i):
                    lin_arr[id] = p(id)

            isClose = True
        elif isClose:
            isClose = False
            start = i

    if not isClose:
        i = len(y)
        arr = y[start:i]

        x = list(range(start, i))
        z = np.polyfit(x, np.array(arr), 1)
        p = np.poly1d(z)

        for id in range(start, i):
            lin_arr[id] = p(id)


    data_visualizer.visualize(lin_arr)

    return lin_arr


def predict_labels(y):
    labels = np.ones((len(y)))
    labels = np.multiply(labels, 2)

    isClose = True
    start = 0
    for i in range(len(y)):
        if y[i] == 0:
            if not isClose:
                label = by_apr(y[start:i])

                labels[start:i] = label
            isClose = True
        elif isClose:
            isClose = False
            start = i

    if not isClose:
        i = len(y)
        label = by_apr(y[start:i])
        labels[start:i] = label

    return labels


def scale_labels(orig, labels, window):
    # scale to former value
    n = len(orig)

    scaled_labels = []
    for i in range(n // window):
        for c in range(window):
            scaled_labels.append(labels[i])

    for c in range(n % window):
        scaled_labels.append(labels[len(labels)-1])

    return np.asarray(scaled_labels)


#Сори за г...код
def operations(labels):
    operations = []

    isClose = True
    start = 0
    #Здесь расчитываются все операции
    for i in range(len(labels)):
        if labels[i] == 2:
            if not isClose:
                # print(start, i)
                operations.append([start, i])
            isClose = True
        elif isClose:
            isClose = False
            start = i

    if not isClose:
        i = len(labels)-1
        # print(start, i)
        operations.append([start, i])

    #Здесь объединяю последовательные операции
    #Пример: спуск-стагнация-спуск-спуск-подъем -> спуск -> стагнация
    operations1 = []
    n = len(operations)
    last_label = -1
    last_time = -1
    isClose = True
    for i in range(n):
        # print(i)
        l = labels[operations[i][0]]
        # открываем если закрыто
        if isClose:
            last_label = l
            last_time = i
            isClose = False
        # закрываем если следующий не похож или если это последний элемент
        else:
            if l != last_label:
                operations1.append([operations[last_time][0], operations[i-1][1]])
                last_time = i
                last_label = l
                isClose = True
            if i == n - 1:
                operations1.append([operations[last_time][0], operations[i][1]])

    return operations1


"""
    UP = 0
    DOWN = 1
    STAGNATION or OTHER = 2
"""

def label(id):
    str = "Stagnation"
    if id == 0:
        str = "Growth of values"
    if id == 1:
        str = "Decreasing values"
    return str