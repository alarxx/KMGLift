from prod.kmglift_api import vec2mat, mat2vec, Label, LiftDataPeriods, sameSequence, hms2sec


def test_sameSeq():
    old_periods = LiftDataPeriods(
        periods=[[3316, 3661], [4327, 4342], [8355, 9488], [9734, 11301], [18568, 21144], [23041, 26865],
                 [30143, 30865], [31312, 36822], [57213, 57414], [57985, 58071], [58490, 58830], [59957, 60278],
                 [60469, 60640], [62268, 67352], [68129, 69677], [70129, 71391], [73150, 74486], [78023, 80471],
                 [80754, 82306], [86279, 86397]],
        labels=[Label.DOWN, Label.DOWN, Label.OTHER, Label.DOWN, Label.DOWN, Label.DOWN, Label.DOWN, Label.DOWN,
                Label.DOWN, Label.DOWN, Label.UP, Label.OTHER, Label.OTHER, Label.UP, Label.UP, Label.UP, Label.UP,
                Label.UP, Label.OTHER, Label.UP])
    print(old_periods)

    periods = sameSequence(old_periods)

    print(periods)


if __name__ == "__main__":
    print(hms2sec(seconds=180))