from osgeo import gdal
from osgeo import ogr

# 基本路径
basic_url = r"E:\research\Clip\fenhu"
# 字段名对照设置
Subcatchments = {}
subcatchment = "Subcatch"
# rainGage = "Rain_Gage"
rainGage = "Rain Gage"
outlet = "Outlet"
area = "Area"
# imperv = "F_Imperv"
imperv = "%Imperv"
width = "Width"
# slope = "F_Slope"
slope = "%Slope"
curbLen = "CurbLen"
# snowPack = "Snow_Pack"
snowPack = "Snow Pack"
# 字段名对照设置
Subareas = {}
# nImperv = "N_Imperv"
nImperv = "N-Imperv"
# nPerv = "N_Perv"
nPerv = "N-Perv"
# sImperv = "S_Imperv"
sImperv = "S-Imperv"
# sPerv = "S_Perv"
sPerv = "S-Perv"
pctZero = "PctZero"
routeTo = "RouteTo"
pctRouted = "PctRouted"
# 字段名对照设置
Infiltration = {}
maxRate = "MaxRate"
minRate = "MinRate"
decay = "Decay"
dryTime = "DryTime"
maxInfil = "MaxInfil"
# 字段名对照设置
Junctions = {}
junction = "Junction"
invert = "Invert"
maxDepth = "MaxDepth"
initDepth = "InitDepth"
surDepth = "SurDepth"
aponded = "Aponded"
# 字段名对照设置
Outfalls = {}
outfall = "Outfall"
invertOutfall = "Invert"
typeOutfall = "Type"
# stageData = "Stage_Data"
stageData = "Stage Data"
gated = "Gated"
# 字段名对照设置
Conduits = {}
conduit = "Conduit"
fromNode = "From Node"
# fromNode = "From_Node"
toNode = "To Node"
# toNode = "To_Node"
length = "Length"
roughness = "Roughness"
inOffset = "InOffset"
outOffset = "OutOffset"
initFlow = "InitFlow"
maxFlow = "MaxFlow"
# 字段名对照设置
XSections = {}
link = "Link"
shape = "Shape_1"
geom1 = "Geom1"
geom2 = "Geom2"
geom3 = "Geom3"
geom4 = "Geom4"
barrels = "Barrels"
Coordinates = {}
Polygons = {}
# 显示范围设置
mapContent = "DIMENSIONS 87967.022 46970.862 97014.682 52388.138"

# Junctions
# Coordinates
def readJunctions():
    junctionsLayer = junctionsFile.GetLayerByIndex(0)
    defn = junctionsLayer.GetLayerDefn()
    feature = junctionsLayer.GetNextFeature()
    while feature is not None:
        junctionObj = {
            "Junction": "",
            "Invert": "",
            "MaxDepth": "",
            "InitDepth": "",
            "SurDepth": "",
            "Aponded": ""
        }
        junctionTitle = 0
        for index in range(defn.GetFieldCount()):
            oField = defn.GetFieldDefn(index)
            fieldKey = oField.GetNameRef()
            if fieldKey == junction:
                junctionObj["Junction"] = feature.GetFieldAsString(index)
                junctionTitle = index
            elif fieldKey == invert:
                junctionObj["Invert"] = feature.GetFieldAsString(index)
            elif fieldKey == maxDepth:
                junctionObj["MaxDepth"] = feature.GetFieldAsString(index)
            elif fieldKey == initDepth:
                junctionObj["InitDepth"] = feature.GetFieldAsString(index)
            elif fieldKey == surDepth:
                junctionObj["SurDepth"] = feature.GetFieldAsString(index)
            elif fieldKey == aponded:
                junctionObj["Aponded"] = feature.GetFieldAsString(index)
        Junctions[feature.GetFieldAsString(junctionTitle)] = junctionObj
        geometry = feature.GetGeometryRef()
        coordinateObj = {}
        coordinateObj["Node"] = feature.GetFieldAsString(junctionTitle)
        coordinateObj["X-Coord"] = geometry.GetX()
        coordinateObj["Y-Coord"] = geometry.GetY()
        Coordinates[feature.GetFieldAsString(0)] = coordinateObj
        feature = junctionsLayer.GetNextFeature()
    junctionsFile.Destroy()


# Outfalls
# Coordinates
def readOutfalls():
    outfallsLayer = outfallsFile.GetLayerByIndex(0)
    defn = outfallsLayer.GetLayerDefn()
    feature = outfallsLayer.GetNextFeature()
    while feature is not None:
        outfallObj = {
            "Outfall": "",
            "Invert": "",
            "Type": "",
            "Stage Data": "",
            "Gated": ""
        }
        outfallTitle = 0
        for index in range(defn.GetFieldCount()):
            oField = defn.GetFieldDefn(index)
            fieldKey = oField.GetNameRef()
            if fieldKey == outfall:
                outfallObj["Outfall"] = feature.GetFieldAsString(index)
                outfallTitle = index
            elif fieldKey == invertOutfall:
                outfallObj["Invert"] = feature.GetFieldAsString(index)
            elif fieldKey == typeOutfall:
                outfallObj["Type"] = feature.GetFieldAsString(index)
            elif fieldKey == stageData:
                outfallObj["Stage Data"] = feature.GetFieldAsString(index)
            elif fieldKey == gated:
                outfallObj["Gated"] = feature.GetFieldAsString(index)
        Outfalls[feature.GetFieldAsString(outfallTitle)] = outfallObj
        geometry = feature.GetGeometryRef()
        coordinateObj = {}
        coordinateObj["Node"] = feature.GetFieldAsString(outfallTitle)
        coordinateObj["X-Coord"] = geometry.GetX()
        coordinateObj["Y-Coord"] = geometry.GetY()
        Coordinates[feature.GetFieldAsString(0)] = coordinateObj
        feature = outfallsLayer.GetNextFeature()
    outfallsFile.Destroy()


# Conduits
# XSections
def readConduits():
    conduitsLayer = conduitsFile.GetLayerByIndex(0)
    defn = conduitsLayer.GetLayerDefn()
    feature = conduitsLayer.GetNextFeature()
    while feature is not None:
        conduitObj = {
            "Conduit": "",
            "From Node": "",
            "To Node": "",
            "Length": "",
            "Roughness": "",
            "InOffset": "",
            "OutOffset": "",
            "InitFlow": "",
            "MaxFlow": ""
        }
        xSectionObj = {
            "Link": "",
            "Shape": "",
            "Geom1": "",
            "Geom2": "",
            "Geom3": "",
            "Geom4": "",
            "Barrels": ""
        }
        linkTitle = 0
        for index in range(defn.GetFieldCount()):
            oField = defn.GetFieldDefn(index)
            fieldKey = oField.GetNameRef()
            if fieldKey == conduit:
                conduitObj["Conduit"] = feature.GetFieldAsString(index)
                linkTitle = index
            elif fieldKey == fromNode:
                conduitObj["From Node"] = feature.GetFieldAsString(index)
            elif fieldKey == toNode:
                conduitObj["To Node"] = feature.GetFieldAsString(index)
            elif fieldKey == length:
                conduitObj["Length"] = feature.GetFieldAsString(index)
            elif fieldKey == roughness:
                conduitObj["Roughness"] = feature.GetFieldAsString(index)
            elif fieldKey == inOffset:
                conduitObj["InOffset"] = feature.GetFieldAsString(index)
            elif fieldKey == outOffset:
                conduitObj["OutOffset"] = feature.GetFieldAsString(index)
            elif fieldKey == initFlow:
                conduitObj["InitFlow"] = feature.GetFieldAsString(index)
            elif fieldKey == maxFlow:
                conduitObj["MaxFlow"] = feature.GetFieldAsString(index)
            elif fieldKey == link:
                xSectionObj["Link"] = feature.GetFieldAsString(index)
            elif fieldKey == shape:
                xSectionObj["Shape"] = feature.GetFieldAsString(index)
            elif fieldKey == geom1:
                xSectionObj["Geom1"] = feature.GetFieldAsString(index)
            elif fieldKey == geom2:
                xSectionObj["Geom2"] = feature.GetFieldAsString(index)
            elif fieldKey == geom3:
                xSectionObj["Geom3"] = feature.GetFieldAsString(index)
            elif fieldKey == geom4:
                xSectionObj["Geom4"] = feature.GetFieldAsString(index)
            elif fieldKey == barrels:
                xSectionObj["Barrels"] = feature.GetFieldAsString(index)
        Conduits[feature.GetFieldAsString(linkTitle)] = conduitObj
        XSections[feature.GetFieldAsString(linkTitle)] = xSectionObj
        feature = conduitsLayer.GetNextFeature()

        # geometry = feature.GetGeometryRef()
        # polygonObj = []
        # boundary = geometry.GetBoundary()
        # for index in range(boundary.GetPointCount()):
        #     point = boundary.GetPoint(index)
        #     pointObj = {}
        #     pointObj["Subcatchment"] = feature.GetFieldAsString(subcatchTitle)  # 此处对应字段顺序
        #     pointObj["X-Coord"] = point[0]
        #     pointObj["Y-Coord"] = point[1]
        #     polygonObj.append(pointObj)
        # Polygons[feature.GetFieldAsString(0)] = polygonObj
        # feature = subcatchmentsLayer.GetNextFeature()

    conduitsFile.Destroy()


# Subcatchments
# Subareas
# Infiltration
# Polygons
def readSubcatchments():
    subcatchmentsLayer = subcatchmentsFile.GetLayerByIndex(0)
    defn = subcatchmentsLayer.GetLayerDefn()
    feature = subcatchmentsLayer.GetNextFeature()
    while feature is not None:
        subcatchmentObj = {
            "Subcatchment": "",
            "Rain Gage": "",
            "Outlet": "",
            "Area": "",
            "%Imperv": "",
            "Width": "",
            "%Slope": "",
            "CurbLen": "",
            "Snow Pack": ""
        }
        subareaObj = {
            "Subcatchment": "",
            "N-Imperv": "",
            "N-Perv": "",
            "S-Imperv": "",
            "S-Perv": "",
            "PctZero": "",
            "RouteTo": "",
            "PctRouted": ""
        }
        infiltrationObj = {
            "Subcatchment": "",
            "MaxRate": "",
            "MinRate": "",
            "Decay": "",
            "DryTime": "",
            "MaxInfil": ""
        }
        subcatchTitle = 0
        for index in range(defn.GetFieldCount()):
            oField = defn.GetFieldDefn(index)
            fieldKey = oField.GetNameRef()
            if fieldKey == subcatchment:
                subcatchmentObj["Subcatchment"] = feature.GetFieldAsString(index)
                subareaObj["Subcatchment"] = feature.GetFieldAsString(index)
                infiltrationObj["Subcatchment"] = feature.GetFieldAsString(index)
                subcatchTitle = index
            elif fieldKey == rainGage:
                subcatchmentObj["Rain Gage"] = feature.GetFieldAsString(index)
            elif fieldKey == outlet:
                subcatchmentObj["Outlet"] = feature.GetFieldAsString(index)
            elif fieldKey == area:
                subcatchmentObj["Area"] = feature.GetFieldAsString(index)
            elif fieldKey == imperv:
                subcatchmentObj["%Imperv"] = feature.GetFieldAsString(index)
            elif fieldKey == width:
                subcatchmentObj["Width"] = feature.GetFieldAsString(index)
            elif fieldKey == slope:
                subcatchmentObj["%Slope"] = feature.GetFieldAsString(index)
            elif fieldKey == curbLen:
                subcatchmentObj["CurbLen"] = feature.GetFieldAsString(index)
            elif fieldKey == snowPack:
                subcatchmentObj["Snow Pack"] = feature.GetFieldAsString(index)
            elif fieldKey == nImperv:
                subareaObj["N-Imperv"] = feature.GetFieldAsString(index)
            elif fieldKey == nPerv:
                subareaObj["N-Perv"] = feature.GetFieldAsString(index)
            elif fieldKey == sImperv:
                subareaObj["S-Imperv"] = feature.GetFieldAsString(index)
            elif fieldKey == sPerv:
                subareaObj["S-Perv"] = feature.GetFieldAsString(index)
            elif fieldKey == pctZero:
                subareaObj["PctZero"] = feature.GetFieldAsString(index)
            elif fieldKey == routeTo:
                subareaObj["RouteTo"] = feature.GetFieldAsString(index)
            elif fieldKey == pctRouted:
                subareaObj["PctRouted"] = feature.GetFieldAsString(index)
            elif fieldKey == maxRate:
                infiltrationObj["MaxRate"] = feature.GetFieldAsString(index)
            elif fieldKey == minRate:
                infiltrationObj["MinRate"] = feature.GetFieldAsString(index)
            elif fieldKey == decay:
                infiltrationObj["Decay"] = feature.GetFieldAsString(index)
            elif fieldKey == dryTime:
                infiltrationObj["DryTime"] = feature.GetFieldAsString(index)
            elif fieldKey == maxInfil:
                infiltrationObj["MaxInfil"] = feature.GetFieldAsString(index)
        Subcatchments[feature.GetFieldAsString(subcatchTitle)] = subcatchmentObj
        Subareas[feature.GetFieldAsString(subcatchTitle)] = subareaObj
        Infiltration[feature.GetFieldAsString(subcatchTitle)] = infiltrationObj
        geometry = feature.GetGeometryRef()
        polygonObj = []
        boundary = geometry.GetBoundary()
        for index in range(boundary.GetPointCount()):
            point = boundary.GetPoint(index)
            pointObj = {}
            pointObj["Subcatchment"] = feature.GetFieldAsString(subcatchTitle)  # 此处对应字段顺序
            pointObj["X-Coord"] = point[0]
            pointObj["Y-Coord"] = point[1]
            polygonObj.append(pointObj)
        Polygons[feature.GetFieldAsString(0)] = polygonObj
        feature = subcatchmentsLayer.GetNextFeature()
    subcatchmentsFile.Destroy()


def writeInpFile():
    with open(basic_url+"/result.inp", "w") as f:
        basicContent = "[TITLE]\n" \
                       ";;Project Title/Notes\n" \
                       "\n" \
                       "[OPTIONS]\n" \
                       ";;Option             Value\n" \
                       "FLOW_UNITS           CMS\n" \
                       "INFILTRATION         HORTON\n" \
                       "FLOW_ROUTING         KINWAVE\n" \
                       "LINK_OFFSETS         DEPTH\n" \
                       "MIN_SLOPE            0\n" \
                       "ALLOW_PONDING        NO\n" \
                       "SKIP_STEADY_STATE    NO\n" \
                       "\n" \
                       "START_DATE           10/11/2019\n" \
                       "START_TIME           00:00:00\n" \
                       "REPORT_START_DATE    10/11/2019\n" \
                       "REPORT_START_TIME    00:00:00\n" \
                       "END_DATE             10/11/2019\n" \
                       "END_TIME             06:00:00\n" \
                       "SWEEP_START          1/1\n" \
                       "SWEEP_END            12/31\n" \
                       "DRY_DAYS             0\n" \
                       "REPORT_STEP          00:15:00\n" \
                       "WET_STEP             00:05:00\n" \
                       "DRY_STEP             01:00:00\n" \
                       "ROUTING_STEP         0:00:30 \n" \
                       "\n" \
                       "INERTIAL_DAMPING     PARTIAL\n" \
                       "NORMAL_FLOW_LIMITED  BOTH\n" \
                       "FORCE_MAIN_EQUATION  H-W\n" \
                       "VARIABLE_STEP        0.75\n" \
                       "LENGTHENING_STEP     0\n" \
                       "MIN_SURFAREA         0\n" \
                       "MAX_TRIALS           0\n" \
                       "HEAD_TOLERANCE       0\n" \
                       "SYS_FLOW_TOL         5\n" \
                       "LAT_FLOW_TOL         5\n" \
                       "\n" \
                       "[EVAPORATION]\n" \
                       ";;Evap Data      Parameters\n" \
                       ";;-------------- ----------------\n" \
                       "CONSTANT         0.0\n" \
                       "DRY_ONLY         NO\n"
        midContent = "[REPORT]\n" \
                     ";;Reporting Options\n" \
                     "INPUT      NO\n" \
                     "CONTROLS   NO\n" \
                     "SUBCATCHMENTS ALL\n" \
                     "NODES ALL\n" \
                     "LINKS ALL\n" \
                     "\n" \
                     "[TAGS]\n" \
                     "\n" \
                     "[MAP]\n" \
                     + mapContent + "\n" \
                     "Units      None\n"
        # basic
        f.write(basicContent)
        f.write("\n")
        # SUBCATCHMENTS
        subcatchmentsTitle = "[SUBCATCHMENTS]\n" \
                             ";;Subcatchment   Rain Gage        Outlet           Area     %Imperv  Width    %Slope" \
                             "   CurbLen  Snow Pack     \n" \
                             ";;-------------- ---------------- ---------------- -------- -------- -------- --------" \
                             " -------- ----------------\n"
        f.write(subcatchmentsTitle)
        for key in Subcatchments:
            subcatchmentObj = Subcatchments[key]
            line = ""
            for field in subcatchmentObj:
                line += subcatchmentObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # SUBAREAS
        subareasTitle = "[SUBAREAS]\n" \
                        ";;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo" \
                        "    PctRouted\n" \
                        ";;-------------- ---------- ---------- ---------- ---------- ---------- ----------" \
                        " ----------\n"
        f.write(subareasTitle)
        for key in Subareas:
            areasObj = Subareas[key]
            line = ""
            for field in areasObj:
                line += areasObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # INFILTRATION
        infiltrationTitle = "[INFILTRATION]\n" \
                            ";;Subcatchment   MaxRate    MinRate    Decay      DryTime    MaxInfil\n" \
                            ";;-------------- ---------- ---------- ---------- ---------- ----------\n"
        f.write(infiltrationTitle)
        for key in Infiltration:
            infiltrationObj = Infiltration[key]
            line = ""
            for field in infiltrationObj:
                line += infiltrationObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # JUNCTIONS
        junctionsTitle = "[JUNCTIONS]\n" \
                         ";;Junction       Invert     MaxDepth   InitDepth  SurDepth   Aponded\n" \
                         ";;-------------- ---------- ---------- ---------- ---------- ----------\n"
        f.write(junctionsTitle)
        for key in Junctions:
            junctionObj = Junctions[key]
            line = ""
            for field in junctionObj:
                line += junctionObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # OUTFALLS
        outfallTitle = "[OUTFALLS]\n" \
                       ";;Outfall        Invert     Type       Stage Data       Gated\n" \
                       ";;-------------- ---------- ---------- ---------------- --------\n"
        f.write(outfallTitle)
        for key in Outfalls:
            outfallObj = Outfalls[key]
            line = ""
            for field in outfallObj:
                line += outfallObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # CONDUITS
        conduitsTitle = "[CONDUITS]\n" \
                        ";;Conduit        From Node        To Node          Length     Roughness  InOffset   " \
                        "OutOffset  InitFlow   MaxFlow\n" \
                        ";;-------------- ---------------- ---------------- ---------- ---------- ---------- " \
                        "---------- ---------- ----------\n"
        f.write(conduitsTitle)
        for key in Conduits:
            conduitObj = Conduits[key]
            line = ""
            for field in conduitObj:
                line += conduitObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # XSECTIONS
        xSectionsTitle = "[XSECTIONS]\n" \
                         ";;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels\n" \
                         ";;-------------- ------------ ---------------- ---------- ---------- ---------- ----------\n"
        f.write(xSectionsTitle)
        for key in XSections:
            xSectionObj = XSections[key]
            line = ""
            for field in xSectionObj:
                line += xSectionObj[field] + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # mid
        f.write(midContent)
        f.write("\n")
        # COORDINATES
        coordinatesTitle = "[COORDINATES]\n" \
                           ";;Node           X-Coord            Y-Coord\n" \
                           ";;-------------- ------------------ ------------------\n"
        f.write(coordinatesTitle)
        for key in Coordinates:
            coordinateObj = Coordinates[key]
            line = ""
            for field in coordinateObj:
                line += str(coordinateObj[field]) + "         "
            line += "\n"
            f.write(line)
        f.write("\n")
        # VERTICES
        verticesTitle = "[VERTICES]\n" \
                        ";;Link           X-Coord            Y-Coord\n" \
                        ";;-------------- ------------------ ------------------\n"
        f.write(verticesTitle)
        f.write("\n")
        # Polygon
        polygonsTitle = "[Polygons]\n" \
                        ";;Subcatchment   X-Coord            Y-Coord\n" \
                        ";;-------------- ------------------ ------------------\n"
        f.write(polygonsTitle)
        for key in Polygons:
            polygonObj = Polygons[key]
            for pointObj in polygonObj:
                line = ""
                for field in pointObj:
                    line += str(pointObj[field]) + "         "
                line += "\n"
                f.write(line)
        f.write("\n")


# main
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
gdal.SetConfigOption("SHAPE_ENCODING", "")
ogr.RegisterAll()
driver = ogr.GetDriverByName('ESRI Shapefile')
junctionsFile = driver.Open(basic_url+'/junction.shp')
if junctionsFile is None:
    print("junctions shp read fail!")
else:
    readJunctions()
    
outfallsFile = driver.Open(basic_url+'/outfall.shp')
if outfallsFile is None:
    print("outfalls shp read fail!")
else:
    readOutfalls()
conduitsFile = driver.Open(basic_url+'/conduit.shp')
if conduitsFile is None:
    print("conduits shp read fail!")
else:
    readConduits()
subcatchmentsFile = driver.Open(basic_url+'/subcatch.shp')
if subcatchmentsFile is None:
    print("subcatchments shp read fail!")
else:
    readSubcatchments()
writeInpFile()
