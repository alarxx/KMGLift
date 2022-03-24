import numpy

if __name__ == "__main__":
    arr = [1, 2, 3, 4]

    arr2 = [1, 2, 3]

    arr2[len(arr):] = arr[0:len(arr)]

    print(arr2)

    arr = numpy.array([[1,2,3], [1,2,3], [1, 2, 3]])
    a = arr[0:0+1, 0:0+2]
    print(a)