import geopandas
import sys

# shp转geojson
def shp_to_geojson(shp_path, geoj_path):
    shp = geopandas.read_file(shp_path)
    shp.to_file(geoj_path, driver = "GeoJSON", encoding = "utf-8")
    print('suc')

# geojson转shp
def geojson_to_shp(geoj_path, shp_path):
    geoj = geopandas.read_file(geoj_path)
    geoj.to_file(shp_path, driver = "ESRI Shapefile", encoding = "utf-8")
    print('suc')

def execute(path1, path2, type):
    if type == "ShpToGeoJSON":
        shp_to_geojson(path1, path2)
    elif type == "GeoJSONToShp":
        geojson_to_shp(path1, path2)

if __name__ == '__main__':
    #InputPath OutputPath type
    execute(sys.argv[1], sys.argv[2], sys.argv[3])