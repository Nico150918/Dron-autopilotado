import argparse
import fileProcessor
import flightFactory
import sensor
import SPITransmiter as SPIT
from configVariables import DEFAULT_DATA_VALUE,MAX_SPI_HZ,DEF_SPI_MODULE,DEF_SPI_DISP

def distanceLoop(loop = 1):
    mySens = sensorList[0]
    if loop == 0:
        while True:
            print("Distancia: %.2f cm" % mySens.distanceInCM())
    else:
        for i in range (0,loop):
            print("Distancia: %.2f cm" % mySens.distanceInCM())


def testControl(secDist):
    mySens = sensorList[0]
    while True:
        dist = mySens.distanceInCM()
        if dist < secDist:
            print("Stop")

def decodeData(data):
    arr = [int(dec) for dec in data.split(',')]
    print("Decoded data = " + str(arr))
    return arr

def sendData(data):
    decData = decodeData(data)
    while (True):
        if (mySPI.sendData(decData)):
            print("correcto")
            break
    mySPI.cleanUp()

def defaultWorking(file):
    fp = fileProcessor.FileProcessor(file)
    if not fp.verifyValid():
        print("Error en el formato del JSON")
        return
    else:
        flight = myFlightFactory.createFlight(fp,mySPI,sensorList)
        print(flight.__str__())
        flight.fly()



def cliManager():
    parser = argparse.ArgumentParser()
    parser.add_argument("method",
                        help="metodo que se va a usar \n opciones: distanceLoop / testControl",
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
        distanceLoop(args.loop)
    elif args.method == "testControl":
        testControl(args.secDist)
    elif args.method == "sendData":
        sendData(args.data)
    elif args.method == "default":
        if args.file:
            defaultWorking(args.file)
        else:
            print("El metodo default necesita un archivo -f archivo json o --file archivo json")
    else:
        print("El metodo "+ args.method + " no existe \n los metodos que hay son: distanceLoop")
    for mySens in sensorList:
        mySens.cleanUp()

mySens = sensor.distanceSensor(16,18) #Crear tus sensores
sensorList = [mySens] #Para añadir tantos sensores como los que se dispongan
mySPI = SPIT.SPITransmiter()
myFlightFactory = flightFactory.FlightFactory()
cliManager()