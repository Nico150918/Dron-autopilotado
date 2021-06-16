import sensor
import argparse
import SPITransmiter as SPIT
from configVariables import DEFAULT_DATA_VALUE

def distanceLoop(loop = 1):
    if loop == 0:
        while True:
            print("Distancia: %.2f cm" % mySens.distanceInCM())
    else:
        for i in range (0,loop):
            print("Distancia: %.2f cm" % mySens.distanceInCM())


def testControl(secDist):
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

    args = parser.parse_args()
    if args.method == "distanceLoop":
        distanceLoop(args.loop)
    elif args.method == "testControl":
        testControl(args.secDist)
    elif args.method == "sendData":
        sendData(args.data)
    else:
        print("El metodo "+ args.method + " no existe \n los metodos que hay son: distanceLoop")
    mySens.cleanUp()


mySens = sensor.distanceSensor(16,18)
mySPI = SPIT.SPITransmiter()
cliManager()