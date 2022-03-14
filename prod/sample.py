from prod.kmglift_api import LiftData

if __name__ == "__main__":
    dir = "..\\assets\\KMG\\AKSH-283\\"

    f1 = dir + "weight_09.06.xlsx"
    f2 = dir + "weight_10.06.xlsx"

    liftData = LiftData([f2]) # [f1, f2] для, перетекающих изо дня в день, процессов

    # print(liftData.liftDataSec)
    print(liftData.periods)

    # print_periods(liftData)
    # vis_labels(liftData)