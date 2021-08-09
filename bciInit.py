import os

path = r'E:\research\model\modelCoupling\swmm\node_corrd.txt'
wPath = r'E:\research\model\modelCoupling\swmm\node_corrd.bci'

file = open(path)
for line in file:
    arr = line.split()
    arr1 = [0]*5
    arr1[0] = 'P'
    arr1[1] = arr[1]
    arr1[2] = arr[2]
    arr1[3] = 'QVAR'
    arr1[4] = arr[0]
    with open(wPath, 'a+') as f:
        f.write((' ').join(map(str, arr1)))
        f.write('\n')