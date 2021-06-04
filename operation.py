#rain
import os
def operationRain():
    file = open(r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test2\fenhuRes2.rain")
    wfile = r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test2\fenhuRes3.rain"
    count = 0
    for line in file:
        if count < 2:
            with open(wfile,'a+') as f:
                f.write(line)
        #只保留1500个元素
        elif count >= 2 and count <=1501:
            arr = line.split('\t')
            #处理line,全部赋值为0
            # if float(arr[1])>100:
            #     arr[1] = float(arr[1]) / 1000
            # elif float(arr[1])>10:
            #     arr[1] = float(arr[1]) / 100
            # else:
            #     arr[1] = float(arr[1])/10
            #扩大倍数至35倍
            arr[1] = float(arr[1]) * 35
            str_array = '\t'.join(map(str, arr))
            with open(wfile,'a+') as f:
                f.write(str_array)
        else:
            break
        count += 1

#操作csv数据
def operationCSV():
    wfile = r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\fenhuzjg.rain"
    with open("data/zjg_120_50.csv") as file:
        count = 0
        for line in file:
            print(line)
            arr = line.split(',')
            narr = []
            narr.append(float(arr[1]) * 60)
            narr.append(count * 60)
            count += 1
            with open(wfile, 'a+') as f:
                str_array = '\t'.join(map(str, narr))
                f.write(str_array + '\n')

def operationRainTxt():
    wfile = r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhuRain_5_mm_min.txt"
    with open(r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhuRain_5.txt") as file:
        count = 0
        for line in file:
            print(line)
            arr = line.strip().split('\t')
            narr = []
            narr.append(float(arr[1]) / 5)
            count += 1
            with open(wfile, 'a+') as f:
                str_array = '\t'.join(map(str, narr))
                f.write(str_array + '\n')
    wfile = r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhuRain_5_mm_h.rain"
    with open(r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhuRain_5_mm_min.txt") as file:
        count = 0
        for line in file:
            print(line)
            arr = line.strip().split('\t')
            narr = []
            narr.append(float(arr[0]) * 60)
            narr.append(count * 300)
            count += 1
            with open(wfile, 'a+') as f:
                str_array = '\t'.join(map(str, narr))
                f.write(str_array + '\n')
if __name__ == '__main__':
    operationRainTxt()