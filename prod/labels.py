from enum import Enum


class Label(Enum):
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER = 3


if __name__ == "__main__":
    mem = Label.NODATA
    print(mem.value)
    print(mem.name)
