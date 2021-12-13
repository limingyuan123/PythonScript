import pandas as pd
from pandas import DataFrame
# import gdal
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

def operationPoint():
    path = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_point.xls'
    wPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_point_res_1.txt'

    data = pd.read_excel(path, header=0)
    # print(data.head())
    # print(data.values[0][0], data.values[0][4]-data.values[0][5], data.values[0][5], data.values[0][11], data.values[0][12])
    arr = [0]*5
    rows = len(data.values)
    k = 0
    for i in range(rows):
        arr[k] = data.values[i][0]
        k+=1
        if data.values[i][2] != data.values[i][2]:
            arr[k] = data.values[i][1] - 3
        else:
            arr[k] = data.values[i][1]-data.values[i][2]
        
        k+=1
        if data.values[i][2] != data.values[i][2]:
            # 无井底埋深,设置一个较为大的深度
            arr[k] = 3
        else:
            arr[k] = data.values[i][2]
        k+=1
        arr[k] = data.values[i][3]
        k+=1
        arr[k] = data.values[i][4]
        k = 0
        with open(wPath, 'a+') as f:
            f.write((' ').join(map(str, arr)))
            f.write('\n')

def operationLine():
    path = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_line.xls'
    wPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_line_res_1.txt'

    data = pd.read_excel(path, header=None)
    # print(data.head())
    # print(data.values[0][0], data.values[0][3], data.values[0][4], data.values[0][14], data.values[0][15], data.values[0][31])
    arr = [0]*10
    rows = len(data.values)
    k = 0
    for i in range(rows):
        arr[k] = data.values[i][0]
        k+=1
        arr[k] = data.values[i][1]
        k+=1
        arr[k] = data.values[i][2]
        k+=1
        arr[k] = data.values[i][3] if data.values[i][3] > data.values[i][4] else data.values[i][4]
        k+=1
        arr[k] = data.values[i][5]
        k+=1
        arr[k] = data.values[i][6]
        k+=1
        arr[k] = data.values[i][7]
        k+=1
        arr[k] = data.values[i][8]
        k+=1
        arr[k] = data.values[i][9]
        k+=1
        arr[k] = data.values[i][10]
        k = 0
        with open(wPath, 'a+') as f:
            f.write((' ').join(map(str, arr)))
            f.write('\n')

def getCoor():
    pointPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\ws_pipe_point_res_1.xls'
    linePath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\ws_pipe_line_res_1.xls'
    wPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\ws_pipe_line_res_1_corrRain_2.txt'
    wEIPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\wsEI.txt'

    coor = {}
    pointData = pd.read_excel(pointPath, header=None)
    lineData = pd.read_excel(linePath, header=None)
    pointRows = len(pointData.values)
    lineRows = len(lineData.values)

    for i in range(pointRows):
        coor[pointData.values[i][0]] = {
            'EI':pointData.values[i][1],
            'X-Coordinate':pointData.values[i][3],
            'Y-Coordinate':pointData.values[i][4],
            #定义新的高程，更新高程
            'NEI':None
        }

    for i in range(lineRows):
        inlet = lineData.values[i][1]
        outlet = lineData.values[i][2]
        # for j in range(pointRows):
        arr = [0]*13
        # arrEI = [0] * 1
        arr[0] = lineData.values[i][0]
        arr[1] = lineData.values[i][1]
        arr[2] = lineData.values[i][2]
        arr[3] = lineData.values[i][3]
        arr[4] = lineData.values[i][4]
        if coor.get(inlet, 0) != 0:
            obj = coor.get(inlet, 0)            
            arr[5] = obj['X-Coordinate']
            arr[6] = obj['Y-Coordinate']
            # 如果搞成为空置为0
            if obj['EI'] != obj['EI']:
                arr[9] = 0
                print("line row is " + i)
                coor[inlet]['NEI'] = obj['EI']
                # arrEI[0] = obj['EI']
            elif lineData.values[i][5] - obj['EI'] < 0:
                arr[9] = 0
                coor[inlet]['NEI'] = obj['EI'] - (-1 * (lineData.values[i][5] - obj['EI']))
            else:
                arr[9] = lineData.values[i][5] - obj['EI']
                coor[inlet]['NEI'] = obj['EI']
            
        else:
            arr[5] = 'undefined'
            arr[6] = 'undefined'
            arr[9] = 'undefined'
            coor[inlet]['NEI'] = obj['EI']
        if coor.get(outlet, 0) != 0:
            obj = coor.get(outlet, 0)
            arr[7] = obj['X-Coordinate']
            arr[8] = obj['Y-Coordinate']
            # 处理异常数据
            if obj['EI'] != obj['EI']:
                arr[10] = 0
                print("line row is " + i)
            elif lineData.values[i][6] - obj['EI'] < 0:
                arr[10] = 0
                coor[outlet]['NEI'] = obj['EI'] - (-1 * lineData.values[i][6] - obj['EI'])
            else:
                arr[10] = lineData.values[i][6] - obj['EI']
                coor[outlet]['NEI'] = obj['EI']
            
        else:
            print(i)
            arr[7] = 'undefined'
            arr[8] = 'undefined'
            arr[10] = 'undefined'
            coor[outlet]['NEI'] = obj['EI']
        # 增加Shape与Geom1
        if lineData.values[i][7] == lineData.values[i][7]:
            arr[11] = 'CIRCULAR'
            arr[12] = float(lineData.values[i][7] / 1000)
        else:
            arr[11] = 'RECT_OPEN'
            arr[12] = float(lineData.values[i][8]*lineData.values[i][9] / 1000000)

        with open(wPath, 'a+') as f:
                f.write((' ').join(map(str, arr)))
                f.write('\n')

    for i in range(pointRows):
        point = pointData.values[i][0]
        arr = [0] * 1
        if coor.get(point, 0) != 0:
            obj = coor.get(point, 0)
            arr[0] = obj['NEI']
            with open(wEIPath, 'a+') as f:
                f.write((' ').join(map(str, arr)))
                f.write('\n')
        else:
            print(i)

    # print('')

def pointTransShp():
    #将txt中的数据转换为shp
    # open the excel file
    path = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_point_res_1_del.xls'
    data = pd.read_excel(path, header=None)
    rows = len(data.values)
    # k = 0

    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()

    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(r"E:\research\fenhuData\pipeNetwork\init_res\copy\shp\RainJunction.shp")

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4490)
    #point
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
    for i in range(rows):
        feature.SetField("Junction", data.values[i][0])
        feature.SetField("Invert", data.values[i][1])
        feature.SetField("MaxDepth", data.values[i][2])
        feature.SetField("InitDepth", 0)
        feature.SetField("SurDepth", 0)
        feature.SetField("Aponded", 0)

        # feature.SetField("Name", data.values[i][0])
        # feature.SetField("Invert EI.", data.values[i][1])
        # feature.SetField("Max. Depth", data.values[i][2])
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(data.values[i][3]), float(data.values[i][4]))
        feature.SetGeometry(point)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')

def lineTransShp():
    #将txt中的数据转换为shp
    # open the excel file
    path = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_line_res_1_corrRain_2_del.xls'
    data = pd.read_excel(path,header=None)
    rows = len(data.values)
    # k = 0

    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")

    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(r"E:\research\fenhuData\pipeNetwork\init_res\copy\shp\RainConduits.shp")


    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4490)
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
    fieldInOffset.SetWidth(20)
    fieldInOffset.SetPrecision(3)
    shapLayer.CreateField(fieldInOffset)
    fieldOutOffset = ogr.FieldDefn("OutOffset", ogr.OFTReal)
    fieldOutOffset.SetWidth(20)
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
    for i in range(rows):

        feature.SetField("Conduit", data.values[i][0])
        feature.SetField("From Node", data.values[i][1])
        feature.SetField("To Node", data.values[i][2])
        feature.SetField("Length", data.values[i][4])
        feature.SetField("Roughness", 0.01)
        feature.SetField("InOffset", data.values[i][9])
        feature.SetField("OutOffset", data.values[i][10])
        feature.SetField("InitFlow", 0)
        feature.SetField("InOffset", data.values[i][9])
        feature.SetField("MaxFlow", 0)
        feature.SetField("Link", data.values[i][0])
        feature.SetField("Shape", data.values[i][11])
        feature.SetField("Geom1", data.values[i][12])
        feature.SetField("Geom2", 0)
        feature.SetField("Geom3", 0)
        feature.SetField("Geom4", 0)
        feature.SetField("Barrels", 1)

        polyline = ogr.Geometry(ogr.wkbLineString)
        polyline.AddPoint(float(data.values[i][5]),
                          float(data.values[i][6]))
        polyline.AddPoint(float(data.values[i][7]),
                          float(data.values[i][8]))
        feature.SetGeometry(polyline)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()
    print('suc')

def transInp():
    # 将shp转为inp
    print('toInp')

    # main
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    junctionsFile = driver.Open(r'E:\research\fenhuData\pipeNetwork\init_res\copy\shp\RainJunction.shp')
    if junctionsFile is None:
        print("junctions shp read fail!")
    else:
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
        
    # outfallsFile = driver.Open(basic_url+'/outfall.shp')
    # if outfallsFile is None:
    #     print("outfalls shp read fail!")
    # else:
    #     readOutfalls()
    conduitsFile = driver.Open(r'E:\research\fenhuData\pipeNetwork\init_res\copy\shp\RainConduits.shp')
    if conduitsFile is None:
        print("conduits shp read fail!")
    else:
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
    # subcatchmentsFile = driver.Open(basic_url+'/subcatch.shp')
    # if subcatchmentsFile is None:
    #     print("subcatchments shp read fail!")
    # else:
    #     readSubcatchments()
    writeInpFile()

def writeInpFile():
    with open(r'E:\research\fenhuData\pipeNetwork\init_res\copy\shp\Rain.inp', "w") as f:
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

#删除雨篦以及带雨篦的线
def deleteYB():
    # 从点里面提取出key value 雨篦为0， 其余为1
    pointPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_point_res_1.xls'
    linePath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_line_res_1_corrRain_2.xls'
    wPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_line_res_1_corrRain_2_del.txt'
    pPath = r'E:\research\fenhuData\pipeNetwork\init_res\copy\rain_pipe_point_res_1_del.txt'

    pointData = pd.read_excel(pointPath, header=None)
    lineData = pd.read_excel(linePath, header=None)
    pointRows = len(pointData.values)
    lineRows = len(lineData.values)

    point = {}

    for i in range(pointRows):
        point[pointData.values[i][0]] = {
            'YB':1,
        }
        if pointData.values[i][6] == "雨篦":
            point[pointData.values[i][0]]['YB'] = 0
    # 遍历line表，只要该节点的YB属性为1就存起来
    for i in range(lineRows):
        arr = [0] * 13
        inlet = lineData.values[i][1]
        outlet = lineData.values[i][2]

        if point.get(inlet, 0) != 0 or point.get(outlet, 0) != 0:
            obj1 = point.get(inlet, 0)
            obj2 = point.get(outlet, 0)
            if obj1['YB'] == 1 and obj2['YB'] == 1:
                for j in range(13):
                    arr[j] = lineData.values[i][j]
                with open(wPath, 'a+') as f:
                    f.write((' ').join(map(str, arr)))
                    f.write('\n')

    # 遍历point表，只要该节点的YB属性为1就存起来 
    for i in range(pointRows):
        arr = [0] * 7
        pointKey = pointData.values[i][0]  

        if point.get(pointKey, 0) != 0:
            obj3 = point.get(pointKey, 0)
            if obj3['YB'] == 1:
                for j in range(7):
                    arr[j] = pointData.values[i][j]
                with open(pPath, 'a+') as f:
                    f.write((' ').join(map(str, arr)))
                    f.write('\n')

if __name__ == '__main__':
    
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
    shape = "Shape"
    geom1 = "Geom1"
    geom2 = "Geom2"
    geom3 = "Geom3"
    geom4 = "Geom4"
    barrels = "Barrels"
    Coordinates = {}
    Polygons = {}
    # 显示范围设置
    mapContent = "DIMENSIONS 40579928.573 3434267.896 40581570.587 3436498.891"

    # operationPoint()
    # operationLine()
    # pointTransShp()
    # getCoor()
    # lineTransShp()
    transInp()

    # deleteYB()