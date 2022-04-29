import os
import rasterio as rio
import glob
# input_ascii_path = r'E:\research\model\SWMM\Material\DavidInformation\芝加哥雨型生成器\raindata.txt'
# write_path = r'E:\research\model\SWMM\Material\DavidInformation\芝加哥雨型生成器\raindata_res.txt'
# file = open(input_ascii_path)
# count = 0
# time = 0
# for line in file:
#     num = float(line) * 80
#     with open(write_path, 'a+') as f:
#         if time >= 60:
#             f.write('r1               04/08/2018 1:')
#             f.write(str(time - 60) + '       ' + str(num))
#             time += 1
#             f.write('    ')
#             f.write('\n')
#         else:
#             f.write('r1               04/08/2018 0:')
#             f.write(str(time) + '       ' + str(num))
#             time += 1
#             f.write('    ')
#             f.write('\n')

def rainSWMMToLis():
    input_ascii_path = r'E:\Projects\SWMM_LISFLOOD_Solution\data\test\rain.txt'
    write_path = r'E:\Projects\SWMM_LISFLOOD_Solution\data\test\rain_res.txt'
    file = open(input_ascii_path)
    time = 0
    for line in file:
        arr = line.split()
        
        with open(write_path, 'a+') as f:
                f.write('   ' + arr[len(arr)-1] + '    ' + str(time))
                time += 60
                f.write('\n')


def operationNan():
    files = sorted(glob.glob(r'E:\research\test4\test\*.wd'))
    write_path = r'E:\research\test4\test'
    arr = []
    num = 0
    for file in files:
        openfile = open(file)
        count = 0
        str2 = '#'
        writePath = write_path + '\\' + str(num) + '.wd'
        for line in openfile:
            if count < 6:
                with open(writePath, 'a+') as f:
                    f.write(line)
                count += 1
                continue
            else:
                arr = line.split()
                for i in range(len(arr)):
                    if str2 in arr[i]:
                        arr[i] = 0.001
                
                with open(writePath, 'a+') as f:
                    f.write(('	').join(map(str, arr)))
                    f.write('\n')
        num += 1


def operationNanNan():
    files = sorted(glob.glob(r'E:\Projects\SWMM_LISFLOOD_Solution\Core\test\*.wd'))
    write_path = r'E:\Projects\SWMM_LISFLOOD_Solution\Core\test'
    arr = []
    num = 0
    for file in files:
        openfile = open(file)
        count = 0
        str2 = 'nan'
        writePath = write_path + '\\' + str(num) + '.wd'
        for line in openfile:        
            if count < 6:
                with open(writePath, 'a+') as f:
                    f.write(line)
                count += 1
                continue
            else:
                arr = line.split()
                for i in range(len(arr)):
                    if str2 in arr[i]:
                        arr[i] = 0.001
                
                with open(writePath, 'a+') as f:
                    f.write(('	').join(map(str, arr)))
                    f.write('\n')
        num += 1

def nan():
    input_ascii_path = r'E:\Projects\SWMM_LISFLOOD_Solution\data\test\results4\anli-0005.wd'
    write_path = r'E:\Projects\SWMM_LISFLOOD_Solution\Core\results4\anli-0005_res_noCouple.wd'
    file = open(input_ascii_path)
    count = 0
    str2 = '#'
    for line in file:
        if count < 6:
            with open(write_path, 'a+') as f:
                f.write(line)
            count += 1
            continue
        else:
            arr = line.split()
            for i in range(len(arr)):
                if str2 in arr[i]:
                    arr[i] = 0.000
            
            with open(write_path, 'a+') as f:
                f.write(('	').join(map(str, arr)))
                f.write('\n')

def operationWD():
    input_ascii_path = r'E:\research\fenhuData\anli2waterdepthnooperation.txt'
    write_path = r'E:\research\fenhuData\anli2waterdepthnooperation_res.txt'
    file = open(input_ascii_path)
    count = 0
    for line in file:
        if count > 5:
            arr = line.split()
            arr1 = [0]*len(arr)
            for i in range(0, len(arr)):
                arr1[i] = arr[i]
                if float(arr[i]) == -9999:
                    arr1[i] = arr[i]
                # elif float(arr[i]) < 0.07:
                #     arr1[i] = -9999

                # elif float(arr[i]) < 0.05:
                #     arr1[i] = 0

                # 方案1 大于0.5的删掉 0.05-0.5  /2.5
                # elif float(arr[i]) > 0.5:
                #     arr1[i] = -9999
                else:
                    arr1[i] = float(arr[i])/8.35
                
            with open(write_path, 'a+') as f:
                    f.write((' ').join(map(str, arr1)))
                    f.write('\n')
        else:
            with open(write_path, 'a+') as f:
                count += 1
                f.write(line)

if __name__ == '__main__':
    operationWD()