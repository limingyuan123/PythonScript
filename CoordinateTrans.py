from osgeo import osr
from pyproj import Proj, transform
import json

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

def loadJson():
    with open("meisongGeoJson.json", 'r', encoding='utf8') as load_f:
        new_dict = json.load(load_f)
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
        with open("newMeisong.json", 'w') as write_f:
            json.dump(new_dict, write_f)
            print('suc')
        # print(new_dict)

if __name__ == '__main__':
    loadJson()