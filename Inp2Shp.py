import re
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import sys

Subcatchments = {}
Subareas = {}
Infiltration = {}
Junctions = {}
Outfalls = {}
Conduits = {}
XSections = {}
Coordinates = {}
Polygons = {}


# Subcatchments
def getSubcatchments(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Subcatchment": lineArray[0],
                "Rain Gage": lineArray[1],
                "Outlet": lineArray[2],
                "Area": lineArray[3],
                "%Imperv": lineArray[4],
                "Width": lineArray[5],
                "%Slope": lineArray[6],
                "CurbLen": lineArray[7],
                "Snow Pack": "",
            }
            Subcatchments[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Subareas
def getSubareas(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Subcatchment": lineArray[0],
                "N-Imperv": lineArray[1],
                "N-Perv": lineArray[2],
                "S-Imperv": lineArray[3],
                "S-Perv": lineArray[4],
                "PctZero": lineArray[5],
                "RouteTo": lineArray[6],
                "PctRouted": "",
            }
            Subareas[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Infiltration
def getInfiltration(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            # meisong的格式
            # jsonObj = {
            #     "Subcatchment": lineArray[0],
            #     "MaxRate": lineArray[1],
            #     "MinRate": lineArray[2],
            #     "Decay": lineArray[3],
            #     "DryTime": lineArray[4],
            #     "MaxInfil": lineArray[5],
            # }
            # fenhu格式
            jsonObj = {
                "Subcatchment": lineArray[0],
                "Suction": lineArray[1],
                "Ksat": lineArray[2],
                "IMD": lineArray[3],
            }
            Infiltration[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Junctions
def getJunctions(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Junction": lineArray[0],
                "Invert": lineArray[1],
                "MaxDepth": lineArray[2],
                "InitDepth": lineArray[3],
                "SurDepth": lineArray[4],
                "Aponded": lineArray[5],
            }
            Junctions[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Outfalls
def getOutfalls(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Outfall": lineArray[0],
                "Invert": lineArray[1],
                "Type": lineArray[2],
                "Stage Data": "",
                "Gated": lineArray[3],
            }
            Outfalls[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Conduits
def getConduits(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Conduit": lineArray[0],
                "From Node": lineArray[1],
                "To Node": lineArray[2],
                "Length": lineArray[3],
                "Roughness": lineArray[4],
                "InOffset": lineArray[5],
                "OutOffset": lineArray[6],
                "InitFlow": lineArray[7],
                "MaxFlow": lineArray[8],
            }
            Conduits[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# XSections
def getXSections(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Link": lineArray[0],
                "Shape": lineArray[1],
                "Geom1": lineArray[2],
                "Geom2": lineArray[3],
                "Geom3": lineArray[4],
                "Geom4": lineArray[5],
                "Barrels": lineArray[6],
            }
            XSections[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Coordinates
def getCoordinates(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            lineStr = r.readline()
            lineArray = re.split("\\s+", lineStr)
            jsonObj = {
                "Node": lineArray[0],
                "X-Coord": lineArray[1],
                "Y-Coord": lineArray[2],
            }
            Coordinates[lineArray[0]] = jsonObj
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# Polygons
def getPolygons(r):
    local = r.tell()
    firstWord = r.read(1)
    r.seek(local, 0)
    while firstWord != '\n':
        if firstWord != ";":
            same = 1
            points = []
            lineStr = r.readline()
            name = ""
            while same:
                same = 0
                lineArray = re.split("\\s+", lineStr)
                name = lineArray[0]
                jsonObj = {
                    "Subcatchment": lineArray[0],
                    "X-Coord": lineArray[1],
                    "Y-Coord": lineArray[2],
                }
                points.append(jsonObj)
                local = r.tell()
                nextLineStr = r.readline()
                r.seek(local, 0)
                if nextLineStr != '\n':
                    nextLineArray = re.split("\\s+", nextLineStr)
                    nextName = nextLineArray[0]
                    if name == nextName:
                        same = 1
                        lineStr = r.readline()
            Polygons[name] = points
        else:
            r.readline()
        local = r.tell()
        firstWord = r.read(1)
        r.seek(local, 0)
    r.seek(local, 0)
    return


# junctionsToShp
def junctionsToShp(OutputPath):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(OutputPath + "/" + "#Junction.shp")

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4528)

    shapLayer = ds.CreateLayer("junction", srs, ogr.wkbPoint)
    fieldNode = ogr.FieldDefn("Junction", ogr.OFTString)
    fieldNode.SetWidth(15)
    shapLayer.CreateField(fieldNode)
    fieldInvert = ogr.FieldDefn("Invert", ogr.OFTReal)
    fieldInvert.SetWidth(10)
    fieldInvert.SetPrecision(5)
    shapLayer.CreateField(fieldInvert)
    fieldMaxDepth = ogr.FieldDefn("MaxDepth", ogr.OFTReal)
    fieldMaxDepth.SetWidth(8)
    fieldMaxDepth.SetPrecision(5)
    shapLayer.CreateField(fieldMaxDepth)
    fieldInitDepth = ogr.FieldDefn("InitDepth", ogr.OFTReal)
    fieldInitDepth.SetWidth(8)
    fieldInitDepth.SetPrecision(5)
    shapLayer.CreateField(fieldInitDepth)
    fieldSurDepth = ogr.FieldDefn("SurDepth", ogr.OFTReal)
    fieldSurDepth.SetWidth(8)
    fieldSurDepth.SetPrecision(5)
    shapLayer.CreateField(fieldSurDepth)
    fieldAponded = ogr.FieldDefn("Aponded", ogr.OFTReal)
    fieldAponded.SetWidth(8)
    fieldAponded.SetPrecision(5)
    shapLayer.CreateField(fieldAponded)
    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    for key in Junctions:
        feature.SetField("Junction", Junctions[key]["Junction"])
        feature.SetField("Invert", Junctions[key]["Invert"])
        feature.SetField("MaxDepth", Junctions[key]["MaxDepth"])
        feature.SetField("InitDepth", Junctions[key]["InitDepth"])
        feature.SetField("SurDepth", Junctions[key]["SurDepth"])
        feature.SetField("Aponded", Junctions[key]["Aponded"])
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(Coordinates[key]["X-Coord"]), float(Coordinates[key]["Y-Coord"]))
        feature.SetGeometry(point)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')


# outfallsToShp
def outfallsToShp(OutputPath):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(OutputPath + "/" + "#Outfall.shp")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4528)
    shapLayer = ds.CreateLayer("outfall", srs, ogr.wkbPoint)
    fieldNode = ogr.FieldDefn("Outfall", ogr.OFTString)
    fieldNode.SetWidth(15)
    shapLayer.CreateField(fieldNode)
    fieldInvert = ogr.FieldDefn("Invert", ogr.OFTReal)
    fieldInvert.SetWidth(10)
    fieldInvert.SetPrecision(5)
    shapLayer.CreateField(fieldInvert)
    fieldMaxType = ogr.FieldDefn("Type", ogr.OFTString)
    fieldMaxType.SetWidth(10)
    shapLayer.CreateField(fieldMaxType)
    fieldData = ogr.FieldDefn("Stage Data", ogr.OFTString)
    fieldData.SetWidth(10)
    shapLayer.CreateField(fieldData)
    fieldGated = ogr.FieldDefn("Gated", ogr.OFTString)
    fieldGated.SetWidth(8)
    shapLayer.CreateField(fieldGated)
    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    for key in Outfalls:
        feature.SetField("Outfall", Outfalls[key]["Outfall"])
        feature.SetField("Invert", Outfalls[key]["Invert"])
        feature.SetField("Type", Outfalls[key]["Type"])
        feature.SetField("Stage Data", Outfalls[key]["Stage Data"])
        feature.SetField("Gated", Outfalls[key]["Gated"])
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(Coordinates[key]["X-Coord"]), float(Coordinates[key]["Y-Coord"]))
        feature.SetGeometry(point)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')


# conduitsToShp
def conduitsToShp(OutputPath):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(OutputPath + "/" + "#Conduit.shp")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4528)
    shapLayer = ds.CreateLayer("conduits", srs, ogr.wkbLineString)
    fieldConduit = ogr.FieldDefn("Conduit", ogr.OFTString)
    fieldConduit.SetWidth(15)
    shapLayer.CreateField(fieldConduit)
    fieldFrom = ogr.FieldDefn("From Node", ogr.OFTString)
    fieldFrom.SetWidth(15)
    shapLayer.CreateField(fieldFrom)
    fieldTo = ogr.FieldDefn("To Node", ogr.OFTString)
    fieldTo.SetWidth(15)
    shapLayer.CreateField(fieldTo)
    fieldLength = ogr.FieldDefn("Length", ogr.OFTReal)
    fieldLength.SetWidth(10)
    fieldLength.SetPrecision(4)
    shapLayer.CreateField(fieldLength)
    fieldRoughness = ogr.FieldDefn("Roughness", ogr.OFTReal)
    fieldRoughness.SetWidth(5)
    fieldRoughness.SetPrecision(3)
    shapLayer.CreateField(fieldRoughness)
    fieldInOffset = ogr.FieldDefn("InOffset", ogr.OFTReal)
    fieldInOffset.SetWidth(5)
    fieldInOffset.SetPrecision(3)
    shapLayer.CreateField(fieldInOffset)
    fieldOutOffset = ogr.FieldDefn("OutOffset", ogr.OFTReal)
    fieldOutOffset.SetWidth(5)
    fieldOutOffset.SetPrecision(3)
    shapLayer.CreateField(fieldOutOffset)
    fieldInitFlow = ogr.FieldDefn("InitFlow", ogr.OFTReal)
    fieldInitFlow.SetWidth(5)
    fieldInitFlow.SetPrecision(3)
    shapLayer.CreateField(fieldInitFlow)
    fieldMaxFlow = ogr.FieldDefn("MaxFlow", ogr.OFTReal)
    fieldMaxFlow.SetWidth(5)
    fieldMaxFlow.SetPrecision(3)
    shapLayer.CreateField(fieldMaxFlow)
    fieldConduit = ogr.FieldDefn("Link", ogr.OFTString)
    fieldConduit.SetWidth(15)
    shapLayer.CreateField(fieldConduit)
    fieldShape = ogr.FieldDefn("Shape", ogr.OFTString)
    fieldShape.SetWidth(15)
    shapLayer.CreateField(fieldShape)
    fieldGeom1 = ogr.FieldDefn("Geom1", ogr.OFTReal)
    fieldGeom1.SetWidth(10)
    fieldGeom1.SetPrecision(4)
    shapLayer.CreateField(fieldGeom1)
    fieldGeom2 = ogr.FieldDefn("Geom2", ogr.OFTReal)
    fieldGeom2.SetWidth(10)
    fieldGeom2.SetPrecision(4)
    shapLayer.CreateField(fieldGeom2)
    fieldGeom3 = ogr.FieldDefn("Geom3", ogr.OFTReal)
    fieldGeom3.SetWidth(10)
    fieldGeom3.SetPrecision(4)
    shapLayer.CreateField(fieldGeom3)
    fieldGeom4 = ogr.FieldDefn("Geom4", ogr.OFTReal)
    fieldGeom4.SetWidth(10)
    fieldGeom4.SetPrecision(4)
    shapLayer.CreateField(fieldGeom4)
    fieldBarrels = ogr.FieldDefn("Barrels", ogr.OFTReal)
    fieldBarrels.SetWidth(10)
    fieldBarrels.SetPrecision(4)
    shapLayer.CreateField(fieldBarrels)
    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    for key in Conduits:
        feature.SetField("Conduit", Conduits[key]["Conduit"])
        feature.SetField("From Node", Conduits[key]["From Node"])
        feature.SetField("To Node", Conduits[key]["To Node"])
        feature.SetField("Length", Conduits[key]["Length"])
        feature.SetField("Roughness", Conduits[key]["Roughness"])
        feature.SetField("InOffset", Conduits[key]["InOffset"])
        feature.SetField("OutOffset", Conduits[key]["OutOffset"])
        feature.SetField("InitFlow", Conduits[key]["InitFlow"])
        feature.SetField("InOffset", Conduits[key]["InOffset"])
        feature.SetField("MaxFlow", Conduits[key]["MaxFlow"])
        feature.SetField("Link", XSections[key]["Link"])
        feature.SetField("Shape", XSections[key]["Shape"])
        feature.SetField("Geom1", XSections[key]["Geom1"])
        feature.SetField("Geom2", XSections[key]["Geom2"])
        feature.SetField("Geom3", XSections[key]["Geom3"])
        feature.SetField("Geom4", XSections[key]["Geom4"])
        feature.SetField("Barrels", XSections[key]["Barrels"])
        polyline = ogr.Geometry(ogr.wkbLineString)
        polyline.AddPoint(float(Coordinates[Conduits[key]["From Node"]]["X-Coord"]),
                          float(Coordinates[Conduits[key]["From Node"]]["Y-Coord"]))
        polyline.AddPoint(float(Coordinates[Conduits[key]["To Node"]]["X-Coord"]),
                          float(Coordinates[Conduits[key]["To Node"]]["Y-Coord"]))
        feature.SetGeometry(polyline)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')


# subcatchmentsToShp
def subcatchmentsToShp(OutputPath):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(OutputPath + "/" + "#Subcatch.shp")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4528)
    shapLayer = ds.CreateLayer("subcatchments", srs, ogr.wkbPolygon)
    fieldSubcatchment = ogr.FieldDefn("Subcatch", ogr.OFTString)  # 缩写
    fieldSubcatchment.SetWidth(15)
    shapLayer.CreateField(fieldSubcatchment)
    fieldGage = ogr.FieldDefn("Rain Gage", ogr.OFTString)
    fieldGage.SetWidth(15)
    shapLayer.CreateField(fieldGage)
    fieldOutlet = ogr.FieldDefn("Outlet", ogr.OFTString)
    fieldOutlet.SetWidth(15)
    shapLayer.CreateField(fieldOutlet)
    fieldArea = ogr.FieldDefn("Area", ogr.OFTReal)
    fieldArea.SetWidth(10)
    fieldArea.SetPrecision(4)
    shapLayer.CreateField(fieldArea)
    fieldImperv = ogr.FieldDefn("%Imperv", ogr.OFTReal)
    fieldImperv.SetWidth(6)
    fieldImperv.SetPrecision(2)
    shapLayer.CreateField(fieldImperv)
    fieldWidth = ogr.FieldDefn("Width", ogr.OFTReal)
    fieldWidth.SetWidth(8)
    fieldWidth.SetPrecision(4)
    shapLayer.CreateField(fieldWidth)
    fieldSlope = ogr.FieldDefn("%Slope", ogr.OFTReal)
    fieldSlope.SetWidth(4)
    fieldSlope.SetPrecision(2)
    shapLayer.CreateField(fieldSlope)
    fieldCurbLen = ogr.FieldDefn("CurbLen", ogr.OFTReal)
    fieldCurbLen.SetWidth(4)
    fieldCurbLen.SetPrecision(2)
    shapLayer.CreateField(fieldCurbLen)
    fieldSnow = ogr.FieldDefn("Snow Pack", ogr.OFTString)
    fieldSnow.SetWidth(10)
    shapLayer.CreateField(fieldSnow)
    fieldNImperv = ogr.FieldDefn("N-Imperv", ogr.OFTReal)
    fieldNImperv.SetWidth(5)
    fieldNImperv.SetPrecision(3)
    shapLayer.CreateField(fieldNImperv)
    fieldNPerv = ogr.FieldDefn("N-Perv", ogr.OFTReal)
    fieldNPerv.SetWidth(5)
    fieldNPerv.SetPrecision(3)
    shapLayer.CreateField(fieldNPerv)
    fieldSImperv = ogr.FieldDefn("S-Imperv", ogr.OFTReal)
    fieldSImperv.SetWidth(5)
    fieldSImperv.SetPrecision(3)
    shapLayer.CreateField(fieldSImperv)
    fieldSPerv = ogr.FieldDefn("S-Perv", ogr.OFTReal)
    fieldSPerv.SetWidth(5)
    fieldSPerv.SetPrecision(3)
    shapLayer.CreateField(fieldSPerv)
    fieldPctZero = ogr.FieldDefn("PctZero", ogr.OFTReal)
    fieldPctZero.SetWidth(4)
    fieldPctZero.SetPrecision(2)
    shapLayer.CreateField(fieldPctZero)
    fieldRouteTo = ogr.FieldDefn("RouteTo", ogr.OFTString)
    fieldRouteTo.SetWidth(10)
    shapLayer.CreateField(fieldRouteTo)
    fieldPctRouted = ogr.FieldDefn("PctRouted", ogr.OFTString)
    fieldPctRouted.SetWidth(8)
    shapLayer.CreateField(fieldPctRouted)
    fieldMaxRate = ogr.FieldDefn("MaxRate", ogr.OFTReal)
    fieldMaxRate.SetWidth(5)
    fieldMaxRate.SetPrecision(2)
    shapLayer.CreateField(fieldMaxRate)
    fieldMinRate = ogr.FieldDefn("MinRate", ogr.OFTReal)
    fieldMinRate.SetWidth(5)
    fieldMinRate.SetPrecision(2)
    shapLayer.CreateField(fieldMinRate)
    fieldDecay = ogr.FieldDefn("Decay", ogr.OFTReal)
    fieldDecay.SetWidth(4)
    fieldDecay.SetPrecision(2)
    shapLayer.CreateField(fieldDecay)
    fieldDryTime = ogr.FieldDefn("DryTime", ogr.OFTReal)
    fieldDryTime.SetWidth(4)
    fieldDryTime.SetPrecision(2)
    shapLayer.CreateField(fieldDryTime)
    fieldMaxInfil = ogr.FieldDefn("MaxInfil", ogr.OFTReal)
    fieldMaxInfil.SetWidth(4)
    fieldMaxInfil.SetPrecision(2)
    shapLayer.CreateField(fieldMaxInfil)
    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    for key in Subcatchments:
        feature.SetField("Subcatch", Subcatchments[key]["Subcatchment"])  # 缩写
        feature.SetField("Rain Gage", Subcatchments[key]["Rain Gage"])
        feature.SetField("Outlet", Subcatchments[key]["Outlet"])
        feature.SetField("Area", Subcatchments[key]["Area"])
        feature.SetField("%Imperv", Subcatchments[key]["%Imperv"])
        feature.SetField("Width", Subcatchments[key]["Width"])
        feature.SetField("%Slope", Subcatchments[key]["%Slope"])
        feature.SetField("CurbLen", Subcatchments[key]["CurbLen"])
        feature.SetField("Snow Pack", Subcatchments[key]["Snow Pack"])
        feature.SetField("N-Imperv", Subareas[key]["N-Imperv"])
        feature.SetField("N-Perv", Subareas[key]["N-Perv"])
        feature.SetField("S-Imperv", Subareas[key]["S-Imperv"])
        feature.SetField("S-Perv", Subareas[key]["S-Perv"])
        feature.SetField("PctZero", Subareas[key]["PctZero"])
        feature.SetField("RouteTo", Subareas[key]["RouteTo"])
        feature.SetField("PctRouted", Subareas[key]["PctRouted"])
        # meisong格式
        # feature.SetField("MaxRate", Infiltration[key]["MaxRate"])
        # feature.SetField("MinRate", Infiltration[key]["MinRate"])
        # feature.SetField("Decay", Infiltration[key]["Decay"])
        # feature.SetField("DryTime", Infiltration[key]["DryTime"])
        # feature.SetField("MaxInfil", Infiltration[key]["MaxInfil"])
        # fenhu格式
        feature.SetField("Suction", Infiltration[key]["Suction"])
        feature.SetField("Ksat", Infiltration[key]["Ksat"])
        feature.SetField("IMD", Infiltration[key]["IMD"])
        polygon = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        points = Polygons[key]
        for point in points:
            ring.AddPoint(float(point["X-Coord"]), float(point["Y-Coord"]))
        ring.CloseRings()
        polygon.AddGeometry(ring)
        feature.SetGeometry(polygon)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')


# transToShp
def transToShp(OutputPath):
    junctionsToShp(OutputPath)
    outfallsToShp(OutputPath)
    conduitsToShp(OutputPath)
    subcatchmentsToShp(OutputPath)


# main
def execute(InputPath, OutputPath):
    with open(InputPath, 'r') as f:
        line = f.readline()
        while line:
            if line == "[SUBCATCHMENTS]\n":
                getSubcatchments(f)
            elif line == "[SUBAREAS]\n":
                getSubareas(f)
            elif line == "[INFILTRATION]\n":
                getInfiltration(f)
            elif line == "[JUNCTIONS]\n":
                getJunctions(f)
            elif line == "[OUTFALLS]\n":
                getOutfalls(f)
            elif line == "[CONDUITS]\n":
                getConduits(f)
            elif line == "[XSECTIONS]\n":
                getXSections(f)
            elif line == "[COORDINATES]\n":
                getCoordinates(f)
            elif line == "[Polygons]\n":
                getPolygons(f)
            line = f.readline()
        transToShp(OutputPath)

if __name__ == '__main__':
    #InputPath OutputPath
    execute(sys.argv[1], sys.argv[2])
    # execute(r"E:\research\model\SWMM\SWMMData\network(wushui2).inp", r"E:\research\model\SWMM\SWMMData\programme\wushui")