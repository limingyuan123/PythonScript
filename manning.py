import os
def defineManning():
    file = open(r"E:\research\Clip\manning1.txt")
    wfile = r"E:\research\Clip\buildingTrans1.txt"
    count = 0
    for line in file:
        if count < 6:
            with open(wfile, 'a+') as f:
                f.write(line)
        else:
            arr = line.split(' ')
            for i in range(len(arr)):
                if arr[i] == '1':
                    arr[i] = '0.012'
                elif arr[i] == '2':
                    arr[i] = '0.2'
                elif arr[i] == '3':
                    arr[i] = '0.012'
                elif arr[i] == '4':
                    arr[i] = '0.03'
            with open(wfile, 'a+') as f:
                f.write((' ').join(map(str, arr)))
        count += 1
if __name__ == '__main__':
    defineManning()