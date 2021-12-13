import os

def thresholdFuc(input_ascii, output_file):
    file = open(input_ascii)
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
            with open(output_file, 'a+') as f:
                    f.write((' ').join(map(str, arr1)))
                    f.write('\n')
        else:
            with open(output_file, 'a+') as f:
                count += 1
                f.write(line)

input_ascii_path = r'C:\Users\HP\AppData\Local\ESRI\Desktop10.2\SpatialAnalyst'
wPath = r'C:\Users\HP\AppData\Local\ESRI\Desktop10.2\SpatialAnalyst\res'
files = os.listdir(input_ascii_path)
for f in files:
    if os.path.splitext(f)[1] == '.txt':
        name = os.path.splitext(f)[0]            
        input_ascii = input_ascii_path + '/' + f
        output_file = wPath + '/' + name + '_res.txt'
        thresholdFuc(input_ascii, output_file)