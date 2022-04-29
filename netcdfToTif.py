import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt

import rasterio

nc_data = nc.Dataset("E:\\research\\model\\ANUGA\\fenhu\\fenhu\\cru_ts4.05.1901.1910.pre.dat.nc")
print(nc_data.variables['tmp'])

raw_tmp_data = np.array(nc_data.variables['tmp'])
tmp_missing_value = nc_data.variables['tmp'].missing_value

# 切片
matrix1 = raw_tmp_data[0, :, :][::-1, :]

## 替换缺失值
matrix1[matrix1 == tmp_missing_value] = np.nan

fig, ax = plt.subplots()
ax.imshow(matrix1)

def array2gtiff(array, filename):
    """
    将一个矩阵保存为tiff文件,
    这里还可以设置tiff的crs和transofrm。更多，可以查看rasterio的官网或者下面的这个链接
    https://gis.stackexchange.com/questions/279953/numpy-array-to-gtiff-using-rasterio-without-source-raster
    :param array: shape:(row, col)
    :param filename:
    :return:
    """
    with rasterio.open(filename, 'w', driver='GTiff',
                       height=array.shape[0], width=array.shape[1],
                       count=1, dtype=str(array.dtype)) as f:
        f.write(array, 1)

# test function
array2gtiff(array=matrix1, filename="E:\\research\\model\\ANUGA\\fenhu\\fenhu\\test001.tiff")