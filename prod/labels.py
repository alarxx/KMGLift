from enum import Enum, unique, auto


@unique
class Label(Enum):
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER = 3


if __name__ == "__main__":
    mem = Label.DOWN
    print(mem.value)
    print(mem.name)
