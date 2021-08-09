import os

path = r'E:\research\model\modelCoupling\swmm\30_node_timeSim_9_11.txt'
wPath = r'E:\research\model\modelCoupling\swmm\30_res_timeSim_9_11.txt'

file = open(path)
for line in file:
    if '<<<' in line:
        with open(wPath, 'a+') as f:
            f.write(line)
    elif '-----' in line:
        continue
    else:
        arr = line.split()
        if len(arr)<6:
            continue
        else: 
            arrCopy = [0]*2
            arrCopy[0] = arr[1]
            if 'Time' in line:  
                arrCopy[1] = 'Flooding'
            else:
                arrCopy[1] = arr[3]
            with open(wPath, 'a+') as f:
                f.write((' ').join(map(str, arrCopy)))
                f.write('\n')