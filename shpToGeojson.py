import geopandas
import os

# shapefile转geojson: shapefile路径 geojson路径
def shp_to_geojson(shp_path, geoj_path):
    shp = geopandas.read_file(shp_path)
    shp.to_file(geoj_path, driver="GeoJSON", encoding="utf-8")


# geojson转shapefile: geojson路径 shapefile路径
def geojson_to_shp(geoj_path, shp_path):
    geoj = geopandas.read_file(geoj_path)
    geoj.to_file(shp_path, driver="ESRI Shapefile", encoding="utf-8")

if __name__ == '__main__':   

    #InputPath OutputPath type 投影转经纬度
    path1 = r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhu_5year_gcgs2000\shp_extract'
    path2 = r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\fenhu_5year_gcgs2000\shp_extract\geojson'


    files = os.listdir(path1)
    for f in files:
        if os.path.splitext(f)[1] == '.shp':
            name = os.path.splitext(f)[0]            
            input_raster = path1 + '/' + f
            output_geojson = path2 + '/' + name + '.json'
            shp_to_geojson(input_raster, output_geojson)