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
    matrix_x = zeros((int(raws_x), int(cols_x)), dtype = float)
    matrix_y = zeros((int(raws_y), int(cols_y)), dtype = float)
    matrix_dem = zeros((int(raws_dem), int(cols_dem)), dtype = float)
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
    xlocs = zeros(raws_x*cols_x+raws_y*cols_y, 1)
    ylocs = xlocs
    U = xlocs
    V = xlocs

    for i in range(1, raws_x):
        for j in range(1, cols_x):
            xlocs((i-1)*cols_x + j, 1) = j-0.5
            ylocs((i-1)*cols_x + j, 1) = i
            U((i-1)*cols_x + j, 1) = matrix_x(i, j)
    for i in range(1, raws_y):
        for j in range(1, cols_y):
            xlocs(cols_x*raws_x + (i-1)*cols_y, 1) = j
            ylocs(cols_x*raws_x + (i-1)* cols_y, 1) = i - 0.5
            V(cols_y*raws_x + (i-1) * cols_y + j, 1) = matrix_y(i, j)

    num_flows = nonzero(U+V)
    xlocs2 = zeros(num_flows, 1)
    ylocs2 = xlocs2
    U2 = xlocs2
    V2 = xlocs2
    k = 1

    for i in range(1, cols_x*raws_x + cols_y * raws_y):
        if (U(i, 1) == 0) and (V(i, 1) == 0):
            print('do nothing!')
        else:
            xlocs2(k, 1) = xlocs(i, 1)
            ylocs2(k, 1) = ylocs(i, 1)
            U2(k, 1) = U(i, 1)
            V2(k, 1) = V(i, 1)
            k = k+1

    if k == num_flows + 1:
        print('all is ok')
    else:
        disp('Problem with flows')

    # overlay flow vectors
    disp('Plotting data... if this is taking a long time you may need fewer locations')

    disp('Done')

        
if __name__ == '__main__':
    # draw()
    readAscii()