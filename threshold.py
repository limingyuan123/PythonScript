import os

def thresholdFuc1(input_ascii, output_file):
    file = open(input_ascii)
    count = 0
    for line in file:
        if count > 5:
            arr = line.split()
            arr1 = [0]*len(arr)
            for i in range(0, len(arr)):
                if float(arr[i]) == -9999:
                    arr1[i] = arr[i]
                elif float(arr[i]) > 1 and float(arr[i]) < 20.2:
                    tmp = float(arr[i])
                    tmp /= 100.0
                    tmp *= 30
                    arr1[i] = tmp 
                else:
                    arr1[i] = arr[i]
            with open(output_file, 'a+') as f:
                    f.write((' ').join(map(str, arr1)))
                    f.write('\n')
        else:
            with open(output_file, 'a+') as f:
                count += 1
                f.write(line)

def thresholdFuc2(input_ascii, output_file):
    file = open(input_ascii)
    count = 0
    for line in file:
        if count > 5:
            arr = line.split()
            arr1 = [0]*len(arr)
            for i in range(0, len(arr)):
                if float(arr[i]) == -9999:
                    arr1[i] = arr[i]
                elif float(arr[i]) >= 9.1:
                    tmp = float(arr[i]) - 9.0
                    tmp *= 10.0
                    arr1[i] = tmp
            with open(output_file, 'a+') as f:
                    f.write((' ').join(map(str, arr1)))
                    f.write('\n')
        else:
            with open(output_file, 'a+') as f:
                count += 1
                f.write(line)

def thresholdFuc3(input_ascii, output_file):
    file = open(input_ascii)
    count = 0
    for line in file:
        if count > 5:
            arr = line.split()
            arr1 = [0]*len(arr)
            for i in range(0, len(arr)):
                arr1[i] = arr[i]
                if float(arr[i]) == -9999:
                    arr1[i] = arr[i]
                elif float(arr[i]) < 0.07:
                    arr1[i] = -9999

                # elif float(arr[i]) < 0.05:
                #     arr1[i] = 0

                # 方案1 大于0.5的删掉 0.05-0.5  /2.5
                # elif float(arr[i]) > 0.5:
                #     arr1[i] = -9999
                # else:
                #     arr1[i] = float(arr[i])/2.5
                
            with open(output_file, 'a+') as f:
                    f.write((' ').join(map(str, arr1)))
                    f.write('\n')
        else:
            with open(output_file, 'a+') as f:
                count += 1
                f.write(line)


input_ascii_path = r'E:\research\swmm_lisflood_anli1\nocouple_res_res_res.txt'
wPath = r'E:\research\swmm_lisflood_anli1\nocouple_res_res_res_res1.txt'
# files = os.listdir(input_ascii_path)
# for f in files:
#     if os.path.splitext(f)[1] == '.wd':
#         name = os.path.splitext(f)[0]
#         input_ascii = input_ascii_path + '/' + f
#         output_file = wPath + '/' + name + '_res.wd'
#         thresholdFuc1(input_ascii, output_file)

thresholdFuc3(input_ascii_path, wPath)