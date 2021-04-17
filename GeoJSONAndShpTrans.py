import geopandas

# shp转geojson
def shp_to_geojson(shp_path, geoj_path):
    shp = geopandas.read_file(shp_path)
    shp.to_file(geoj_path, driver = "GeoJSON", encoding = "utf-8")

# geojson转shp
def geojson_to_shp(geoj_path, shp_path):
    geoj = geopandas.read_file(geoj_path)
    geoj.to_file(shp_path, driver = "ESRI Shapefile", encoding = "utf-8")

if __name__ == '__main__':
    geojson_to_shp(r"C:\Users\HP\Desktop\newMeisong.json", r"C:\Users\HP\Desktop\out")