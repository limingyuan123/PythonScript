from osgeo import osr

def coordinateTrans(arr):
    source = osr.SpatialReference()
    source.ImportFromEPSG(3857)

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
    ct = transform.TransformPoint(arr[0], arr[1])
    print(ct)

if __name__ == '__main__':
    coordinateTrans([422950, 197600])
