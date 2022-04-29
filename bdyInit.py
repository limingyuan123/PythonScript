import os

path = r'E:\research\model\modelCoupling\文件型耦合实验\flooding_res.txt'
wPath = r'E:\research\model\modelCoupling\文件型耦合实验\flooding_res.bdy'

file = open(path)
count = 1
for line in file:
    if "<<<" in line:
        count = 1
        arr1 = line.split()
        with open(wPath, 'a+') as f:
            f.write(arr1[2] + '\n')
    elif "Time" in line:
        with open(wPath, 'a+') as f:
            f.write("25     seconds" + '\n')
            f.write("0     0" + '\n')
    else:
        arr2 = line.split()
        arr3 = [0] * 2
        arr3[0] = arr2[1]
        arr3[1] = 5*(count)*60
        count = count + 1
        with open(wPath, 'a+') as f:
            f.write((' ').join(map(str, arr3)))
            f.write('\n')

