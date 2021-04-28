import os
#init depth
file = open(r"E:\research\model\lisflood-fp\fenhuTestModelData\fenhuCopy.depth")
wfile = r"E:\research\model\lisflood-fp\fenhuTestModelData\fenhuRes.depth"
count = 0
for line in file:
    count += 1    
    if count > 6:
        arr = line.split(' ')
        #处理line,全部赋值为0
        arr = [0] * len(arr)
        str_array = ' '.join(map(str, arr))
        with open(wfile,'a+') as f:
            f.write(str_array + '\n')
    else:
        with open(wfile,'a+') as f:
            f.write(line)