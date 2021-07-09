import json

class FileProcessor:

    def __init__(self,fileLocation = "default.json"):
        self.fileName = fileLocation.split(sep='/').pop()
        try:
            with open(fileLocation) as jsonFile:
                self.jsonText = json.load(jsonFile)
                jsonFile.close()
        except:
            print("Ese archivo no existe, prueba con uno nuevo")

    def getVal(self,key):
        return self.jsonText[key]

    def printJSON(self):
        print("El contenido del archivo",self.fileName.replace(".json",''),"es:")
        for key in self.jsonText:
            print(key+":",self.jsonText[key])

    #Para garantizar que el formato es correcto
    def getKeys(self):
        return [x for x in self.jsonText]

    def verifyValid(self):
        return True

"""
import sys
fp = FileProcessor(sys.argv[1])
fp.printJSON()
"""
