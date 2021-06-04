import matplotlib.pyplot as plt

import cartopy.crs as ccrs
from cartopy.examples.arrows import sample_data

from numpy import *

def draw():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator())
    
    ax.set_extent([-90, 75, 10, 85], crs = ccrs.Mercator())
    ax.coastlines()

    x, y, u, v, vector_crs = sample_data(shape=(80, 100))
    magnitude = (u ** 2 + v ** 2) ** 0.5
    ax.streamplot(x, y, u, v, transform = vector_crs, linewidth = 2, density = 2, color = magnitude)
    plt.show()
def readAscii():
    f1 = open(r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\results9\fenhu-0002.Qx')
    f2 = open(r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\results9\fenhu-0002.Qy')
    f3 = open(r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhu.asc')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    lines3 = f3.readlines()
    cols_x = 0
    raws_x = 0
    cols_y = 0
    raws_y = 0
    cols_dem = 0
    raws_dem = 0
    count = 0
    for line in lines1:
        if count<2:
            arr = line.strip().split('         ')
            if arr[0] == "ncols":
                cols_x = arr[1]
            else:
                raws_x = arr[1]
        else:
            break
        count += 1
    count = 0
    for line in lines2:
        if count<2:
            arr = line.strip().split('         ')
            if arr[0] == "ncols":
                cols_y = arr[1]
            else:
                raws_y = arr[1]
        else:
            break
        count += 1
    count = 0
    for line in lines3:
        if count<2:
            arr = line.strip().split('         ')
            if arr[0] == "ncols":
                cols_dem = arr[1]
            else:
                raws_dem = arr[1]
        else:
            break
        count += 1
    raws_x = int(raws_x)
    cols_x = int(cols_x)
    raws_y = int(raws_y)
    cols_y = int(cols_y)
    raws_dem = int(raws_dem)
    cols_dem = int(cols_dem)
    matrix_x = zeros((raws_x, cols_x), dtype = float)
    matrix_y = zeros((raws_y, cols_y), dtype = float)
    matrix_dem = zeros((raws_dem, cols_dem), dtype = float)
    count = 0
    x_row = 0
    y_row = 0
    dem_row = 0
    for line in lines1:
        if count > 5:
            list = line.strip('\n').split('\t')
            list.pop()
            matrix_x[x_row:] = list[0:]
            x_row += 1
        count+=1
    count = 0
    for line in lines2:
        if count > 5:
            list = line.strip('\n').split('\t')
            list.pop()
            matrix_y[y_row:] = list[0:]
            y_row += 1
        count+=1
    count = 0
    for line in lines3:
        if count > 5:
            list = line.strip('\n').split(' ')
            list.pop()
            matrix_dem[dem_row:] = list[0:]
            dem_row += 1
        count+=1
    print('ok')
    # calculate flow vectors
    xlocs = zeros((raws_x*cols_x+raws_y*cols_y, 1), float)
    ylocs = xlocs.copy()
    U = xlocs.copy()
    V = xlocs.copy()

    for i in range(0, raws_x):
        for j in range(0, cols_x):
            xlocs[(i)*cols_x + j][0] = j + 0.5
            ylocs[(i)*cols_x + j][0] = i + 1
            U[(i)*cols_x + j][0] = matrix_x[i][j]
    for i in range(0, raws_y):
        for j in range(0, cols_y):
            xlocs[cols_x*raws_x + i*cols_y + j][0] = j + 1
            ylocs[cols_x*raws_x + i*cols_y + j][0] = i + 0.5
            V[cols_y*raws_x + i * cols_y + j][0] = matrix_y[i][j]
    nozero = nonzero(matrix_add(U, V, len(U), len(U[0])))
    num_flows = len(nozero[0])
    xlocs2 = zeros((num_flows, 1), float)
    ylocs2 = xlocs2.copy()
    U2 = xlocs2.copy()
    V2 = xlocs2.copy()
    k = 1

    for i in range(0, cols_x*raws_x + cols_y * raws_y):
        if (U[i][0] == 0) and (V[i][0] == 0):
            print('do nothing!')
        elif i<=k:
            xlocs2[k][0] = xlocs[i][0]
            ylocs2[k][0]  = ylocs[i][0]
            U2[k][0]  = U[i][0]
            V2[k][0]  = V[i][0]
            k = k+1
        else:
            break

    if k == num_flows + 1:
        print('all is ok')
    else:
        disp('Problem with flows')

    # overlay flow vectors
    disp('Plotting data... if this is taking a long time you may need fewer locations')

    disp('Done')

def matrix_add(X,Y, raw, col):
    result = zeros((raw, col), float)

    for i in range(len(X)): # 迭代输出行，矩阵当中，是由三个列表所呈现的。
        for j in range(len(X[0])): # 迭代输出列，访问大列表当中 每个列表的第一个元素，即为列
            result[i][j] = X[i][j]+Y[i][j] #X下标对应的数字，加上Y下标对应的数字 即为所求
    return result
if __name__ == '__main__':
    # draw()
    readAscii()