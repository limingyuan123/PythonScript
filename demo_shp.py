from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import pandas as pd
import os
import math
import numpy as np
# from scipy.spatial import Delaunay
# import scipy as sp
from shapely import wkt, geometry
import shapely
from shapely.ops import cascaded_union

import matplotlib as mpl
import matplotlib.pyplot as plt 
# from mpl_toolkits.basemap import Basemap 
# from scipy.special import binom
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase
poDS = None
# try:
out_flow_map_file = r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\arrow.shp'
file = open(r"E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\dataVisualFenhu.txt")

shpName = 'testRes.shp'
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
gdal.SetConfigOption("SHAPE_ENCODING", "")

pszDriverName = "ESRI Shapefile"
ogr.RegisterAll()
poDriver = ogr.GetDriverByName(pszDriverName)
poDS = poDriver.CreateDataSource(out_flow_map_file)

geomType = ogr.wkbLineString
srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
srs = osr.SpatialReference(srs_str)
poLayer = poDS.CreateLayer(shpName, srs, geomType)

#oField1 = ogr.FieldDefn("count", ogr.OFTInteger)
#oField2 = ogr.FieldDefn("percentage", ogr.OFTReal)
#oField3 = ogr.FieldDefn("sink_id", ogr.OFTInteger)
#oField4 = ogr.FieldDefn("source_id", ogr.OFTInteger)
#poLayer.CreateField(oField1, 1)
#poLayer.CreateField(oField2, 1)
#poLayer.CreateField(oField3, 1)
#poLayer.CreateField(oField4, 1)

oDefn = poLayer.GetLayerDefn()

lines = file.readlines()
for line in lines:
	line = line.strip().split('\t')
	temp_x1 = float(line[0])
	temp_y1 = float(line[1])
	temp_x2 = float(line[2])
	temp_y2 = float(line[3])

	tempGeom = ogr.Geometry(ogr.wkbLineString)
	tempGeom.SetPoint(0, temp_x1, temp_y1, 0)
	tempGeom.SetPoint(1, temp_x2, temp_y2, 0)
	
	tempFeature = ogr.Feature(oDefn)
	tempFeature.SetGeometry(tempGeom)
	
	poLayer.CreateFeature(tempFeature)
	del tempFeature

poDS.FlushCache()
del poDS
# except:
# 	if poDS != None: del poDS