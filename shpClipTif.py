from osgeo import gdal
import os
import shapefile
input_shape = r"E:\research\Clip\wd\root_town2.shp" 
# output_raster=r'E:\research\test.tif'
output_raster_path=r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhu_5year_gcgs2000\clip'
# tif输入路径，打开文件
input_raster_path = r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhu_5year_gcgs2000"


files = os.listdir(input_raster_path)
# 开始裁剪，裁剪代码仅需一行，遍历裁剪即可 对应于ArcGIS的蒙版裁剪功能
for f in files:
    if os.path.splitext(f)[1] == '.tif':
        name = os.path.splitext(f)[0]
        input_raster = input_raster_path + '/' + f
        # 矢量文件路径，打开矢量文件
        input_raster = gdal.Open(input_raster)
        output_raster = output_raster_path + '/' + name + '.tif'
        ds = gdal.Warp(output_raster,
                    input_raster,
                    format = 'GTiff',
                    cutlineDSName = input_shape,
                    cutlineWhere="FIELD = 'whatever'",
                    dstNodata = 0)
# 关闭文件
ds=None 