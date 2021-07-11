import argparse
import fileProcessor
import flightFactory
import sensor
import SPITransmiter as SPIT
from configVariables import DEFAULT_DATA_VALUE,MAX_SPI_HZ,DEF_SPI_MODULE,DEF_SPI_DISP
class main():
    def __init__(self):
        self.mySens = sensor.distanceSensor(16, 18)  # Crear tus sensores
        self.sensorList = [self.mySens]  # Para añadir tantos sensores como los que se dispongan
        self.mySPI = SPIT.SPITransmiter()
        self.myFlightFactory = flightFactory.FlightFactory()
        self.cliManager()

    def distanceLoop(self,loop = 1):
        mySens = self.sensorList[0]
        if loop == 0:
            while True:
                print("Distancia: %.2f cm" % mySens.distanceInCM())
        else:
            for i in range (0,loop):
                print("Distancia: %.2f cm" % mySens.distanceInCM())


    def testControl(self,secDist):
        mySens = self.sensorList[0]
        while True:
            dist = mySens.distanceInCM()
            if dist < secDist:
                print("Stop")

    def decodeData(self,data):
        arr = [int(dec) for dec in data.split(',')]
        print("Decoded data = " + str(arr))
        return arr

    def sendData(self,data):
        decData = self.decodeData(data)
        while (True):
            if (self.mySPI.sendData(decData)):
                print("correcto")
                break
        self.mySPI.cleanUp()

    def defaultWorking(self,file):
        fp = fileProcessor.FileProcessor(file)
        if not fp.verifyValid():
            print("Error en el formato del JSON")
            return
        else:
            flight = self.myFlightFactory.createFlight(fp,self.mySPI,self.sensorList)
            print(flight.__str__())
            flight.fly()



    def cliManager(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("method",
                            help="metodo que se va a usar \n opciones: distanceLoop / testControl / sendData / default",
                            action="store",type=str)
        parser.add_argument("-l", "--loop",
                            help="numero de iteraciones, por defecto infinitas (solo se usa en distanceLoop)",
                            action="store",
                            default=0,
                            type=int)
        parser.add_argument("-sd", "--secDist",
                            help="distancia en la que se hara el stop en caso de estar demasiado cerca de la pared valor por defecto 100cm",
                            action="store",
                            default=100,
                            type=int)
        parser.add_argument("-d", "--data",
                            help="...",
                            action="store",
                            default=DEFAULT_DATA_VALUE,
                            type=str)
        parser.add_argument("-f", "--file",
                            help="...",
                            action="store",
                            type=str)

        args = parser.parse_args()
        if args.method == "distanceLoop":
            self.distanceLoop(args.loop)
        elif args.method == "testControl":
            self.testControl(args.secDist)
        elif args.method == "sendData":
            self.sendData(args.data)
        elif args.method == "default":
            if args.file:
                self.defaultWorking(args.file)
            else:
                print("El metodo default necesita un archivo -f archivo json o --file archivo json")
        else:
            print("El metodo "+ args.method + " no existe \n los metodos que hay son: distanceLoop")
        for mySens in self.sensorList:
            mySens.cleanUp()

if __name__ == "__main__":
    myMain = main()