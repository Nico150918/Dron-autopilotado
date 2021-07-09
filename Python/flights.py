import time
from configVariables import ENDVAL
class flight:

    def __init__(self,instructions,SPI,sensorList):
        self.instrutions = instructions
        self.SPI = SPI


    def fly(self):
        for instruction in self.instrutions:
            duration = instruction["duration"]
            values = instruction["values"]
            if len(values) < 8 and values[len(values)-1] <= 100:
                values.add(ENDVAL)
                print("Añadiendo end val")
            self.SPI.sendData(values)
            print("Sleep",duration,"s")
            time.sleep(float(duration))

    def __str__(self):
        print("Vuelo normal:\n instrucciones:",self.instrutions)

class flightLoop(flight):

    def __init__(self, times, *args, **kwargs):
        super(flightLoop, self).__init__(*args, **kwargs)
        self.times = int(times)

    def fly(self):
        for i in range(1,self.times):
            for instruction in self.instrutions:
                duration = instruction["duration"]
                values = instruction["values"]
                if len(values) < 8 and values[len(values)-1] <= 100:
                    values.add(ENDVAL)
                    print("Añadiendo end val")
                self.SPI.sendData(values)
                print("Sleep",duration,"s")
                time.sleep(float(duration))

    def __str__(self):
        print("Vuelo bucle:\n instrucciones:",self.instrutions,"\n Times:",self.times)

class flightDistance(flight):

    def __init__(self, *args, **kwargs):
        super(flight, self).__init__(*args, **kwargs)

    def fly(self):
        for i in range(1,self.times):
            for instruction in self.instrutions:
                duration = instruction["duration"]
                values = instruction["values"]
                if len(values) < 8 and values[len(values)-1] <= 100:
                    values.add(ENDVAL)
                    print("Añadiendo end val")
                self.SPI.sendData(values)
                print("Sleep",duration,"s")
                time.sleep(float(duration))

    def __str__(self):
        print("Vuelo bucle:\n instrucciones:",self.instrutions,"\n Times:",self.times)

