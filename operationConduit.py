import json
import os

def loadJson(path):
    with open(path, 'r', encoding='utf8') as load_f:
        new_dictTop = json.load(load_f)
        new_dict = new_dictTop["features"]
        wfile = r"E:\Projects\PythonScript\res.txt"
        
        for item in new_dict:
            print(item)
            with open(wfile, 'a+') as f:
                f.write(item["properties"]["Conduit"] + " " + str(item["geometry"]["coordinates"][0][0]) + "    " + str(item["geometry"]["coordinates"][0][1]) + "\n")
                f.write(item["properties"]["Conduit"] + " " + str(item["geometry"]["coordinates"][1][0]) + "    " + str(item["geometry"]["coordinates"][1][1]) + "\n")
                
if __name__ == '__main__':
    loadJson(r"E:\Projects\PythonScript\#Conduit.json")