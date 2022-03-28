from prod.kmglift_api import vec2mat, mat2vec

if __name__ == "__main__":
    arr = [0.1, 0.2, 0.3, 0.4, 0.1]
    mat = vec2mat(arr, isPlot=True)
    print(mat)
    res = mat2vec(mat)

    print(arr)
    print(res)