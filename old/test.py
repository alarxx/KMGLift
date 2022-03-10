from enum import Enum, unique


@unique
class Label(Enum):
    NODATA = 0
    DOWN = 1
    UP = 2
    OTHER = 3


if __name__ == "__main__":
    if Label.UP == Label.UP:
        print("lol")