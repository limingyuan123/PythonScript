from osgeo import osr
import json
import sys

def coordinateTrans(arr):
    source = osr.SpatialReference()
    source.ImportFromEPSG(3857)

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
    ct = transform.TransformPoint(arr[0], arr[1])
    ctList = list(ct)
    ctList.pop()
    tmp = ctList[0]
    ctList[0] = ctList[1]
    ctList[1] = tmp
    return ctList
# 转变inp导出的shp的geojson
def loadJson(path1, path2, type):
    with open(path1, 'r', encoding='utf8') as load_f:
        new_dictTop = json.load(load_f)
        new_dict = new_dictTop["features"]
        
        for item in new_dict:
            #加属性name
            #Conduit
            item['properties']['name'] = item['properties'][type]
            #Junction
            # item['properties']['name'] = item['properties']['Junction']
            #Outfall
            # item['properties']['name'] = item['properties']['Outfall']
            #Subcatch
            # item['properties']['name'] = item['properties']['Subcatch']

            if item['geometry']['type'] == 'Point':
                out = coordinateTrans(item['geometry']['coordinates'])
                item['geometry']['coordinates'] = out
            elif item['geometry']['type'] == 'LineString':
                Line = item['geometry']['coordinates']
                newLine = []
                for line in Line:
                    newLine.append(coordinateTrans(line))
                item['geometry']['coordinates'] = newLine
            elif item['geometry']['type'] == 'MultiLineString':
                MutiLine = item['geometry']['coordinates']
                NewMutiLine = []
                for mutiline in MutiLine:
                    newSonMutiLine = []
                    for sonMutiLine in mutiline:
                        newSonMutiLine.append(coordinateTrans(sonMutiLine))
                    NewMutiLine.append(newSonMutiLine)
                item['geometry']['coordinates'] = NewMutiLine
            elif item['geometry']['type'] == 'Polygon':
                ployList = item['geometry']['coordinates'][0]
                newPloyList = []
                for poly in ployList:
                    newPloyList.append(coordinateTrans(poly))
                item['geometry']['coordinates'][0] = newPloyList
        with open(path2, 'w') as write_f:
            json.dump(new_dictTop, write_f)
            print('suc')

# 转变disp中的坐标
def loadJson2(path1, path2):
    with open(path1, 'r', encoding='utf8') as load_f:
        new_dictTop = json.load(load_f)
        new_dict = new_dictTop["GeoJson"]
        
        for item in new_dict:
            if item['geometry']['type'] == 'Point':
                out = coordinateTrans(item['geometry']['coordinates'])
                item['geometry']['coordinates'] = out
            elif item['geometry']['type'] == 'LineString':
                Line = item['geometry']['coordinates']
                newLine = []
                for line in Line:
                    newLine.append(coordinateTrans(line))
                item['geometry']['coordinates'] = newLine
            elif item['geometry']['type'] == 'MultiLineString':
                MutiLine = item['geometry']['coordinates']
                NewMutiLine = []
                for mutiline in MutiLine:
                    newSonMutiLine = []
                    for sonMutiLine in mutiline:
                        newSonMutiLine.append(coordinateTrans(sonMutiLine))
                    NewMutiLine.append(newSonMutiLine)
                item['geometry']['coordinates'] = NewMutiLine
            elif item['geometry']['type'] == 'Polygon':
                ployList = item['geometry']['coordinates'][0]
                newPloyList = []
                for poly in ployList:
                    newPloyList.append(coordinateTrans(poly))
                item['geometry']['coordinates'][0] = newPloyList
        with open(path2, 'w') as write_f:
            json.dump(new_dictTop, write_f)
            print('suc')
            
def execute(path1, path2):
    type = path1.split("#")[1].split(".")[0]
    loadJson(path1, path2, type)

def coordinate(coor1, coor2):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4528)

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
    ct = transform.TransformPoint(coor1, coor2)
    print(ct)
def corrdin(coor1, coor2):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(102100)

    transform = osr.CoordinateTransformation(source, target)
    ct = transform.TransformPoint(coor1, coor2)
    print(ct)
def operaDispCorr(path1, path2):    
    loadJson2(path1, path2)
if __name__ == '__main__':
    #InputPath OutputPath type 投影转经纬度
    execute(sys.argv[1], sys.argv[2])
    # operaDispCorr(r"E:\research\model\SWMM\display\result_5.disp", r"E:\research\model\SWMM\display\result_5_trans.disp")
    # coordinate(3434862.323, 40580992.82)
    # corrdin(31.032280067761373, 120.8483257733613)