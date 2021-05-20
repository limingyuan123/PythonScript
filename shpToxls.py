import shapefile  # 使用pyshp
import geopandas as gpd
segpath = r"E:\research\Clip\point2.shp"
# print(file.fields)# 输出所有字段信息
# print(file.record(0)[0])# 第一个对象的第一个属性值
segshape = gpd.read_file(segpath)
seggeoms = segshape.geometry.values
print('ok')