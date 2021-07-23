import json
from configVariables import TIPOS_DE_VUELO_IMPLEMENTADO

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
    def getKeys(self,js):
        return [x for x in js]

    def verifyValid(self):
        keys = self.getKeys(self.jsonText)
        correcto = True
        if "type" not in keys:
            correcto = False
            print("Error, falta el atributo type, ej: \"type\":\"default\" ")
        elif self.getVal("type") in TIPOS_DE_VUELO_IMPLEMENTADO:

            # verificamos que si es un loop tiene el atruibuto times
            if "loop" in self.getVal("type").lower() and "times" not in keys:
                correcto = False
                print("Error, falta el atributo times, ej: \"times\":5")

            #si tiene instrucciones verificamos que todas sean correctas
            if "instructions" in keys and len(self.getVal("instructions")) > 0:
                for instruction in self.getVal("instructions"):
                    instructionKeys = self.getKeys(instruction)
                    #Comprobamos que cada instruccion tenga los valores
                    if "values" not in instructionKeys:
                        correcto = False
                        print("Error, falta el valor duration en la instruccion:", instruction)

                    #verificamos si esta el atribunto distance en caso de que el vuelo lo requiera
                    if "distance" in self.getVal("type") and "distance" not in instructionKeys:
                        correcto = False
                        print("Error, falta el valor distance en la instruccion:", instruction)

                    # verificamos si esta el atribunto duration para vuelos que no funcionan por distancia
                    if "distance" not in self.getVal("type") and "duration" not in instructionKeys:
                        correcto = False
                        print("Error, falta el valor duration en la instruccion:",instruction)

            #si no tiene instrucciones
            else:
                correcto = False
                print("Error, el vuelo no tiene instruccionesm, ej: \"instrucciones\":\"instructions\": \n\t[{\n\t\t\"duration\": 5,\n\t\t\"values\" : [10,20,30,40,50,60,70,80]\n\t}]\"")

        else:
            correcto = False
            print("Error, ese tipo de vuelo no existe.\n Prueba con:",TIPOS_DE_VUELO_IMPLEMENTADO)
        if correcto:
            print("Vuelo correcto")
        return correcto

'''
import sys
fp = FileProcessor(sys.argv[1])
fp.verifyValid()
'''
