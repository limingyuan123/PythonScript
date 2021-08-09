import os

path = r'E:\research\50_year\ascii\23.txt'
wPath = r'E:\research\50_year\ascii\23_res.txt'

file = open(path)
count = 0
for line in file:
    if count > 5:
        arr = line.split()
        arr1 = [0]*len(arr)
        for i in range(0, len(arr)):
            if float(arr[i]) == -9999:
                arr1[i] = arr[i]
            elif float(arr[i]) < 0.35:
                arr1[i] = -9999
            else:
                arr1[i] = arr[i]
        with open(wPath, 'a+') as f:
                f.write((' ').join(map(str, arr1)))
                f.write('\n')
    else:
        with open(wPath, 'a+') as f:
            count += 1
            f.write(line)