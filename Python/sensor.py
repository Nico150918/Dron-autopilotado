# Importamos la paquteria necesaria
import RPi.GPIO as GPIO
import time
import configVariables as conf

class distanceSensor:

    def __init__(self, trig = 16, echo = 18):
        self.TRIG = trig
        self.ECHO = echo
        GPIO.setmode(GPIO.BCM)  # Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi
        GPIO.setup(self.TRIG, GPIO.OUT)  # Configuramos el pin TRIG como una salida
        GPIO.setup(self.ECHO, GPIO.IN)  # Configuramos el pin ECHO como una salida
        print("init")


    def initializeSensor(self):
        GPIO.output(self.TRIG, GPIO.LOW)
        time.sleep(0.5) #tiempo para que se estabilice

        # Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
        GPIO.output(self.TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, GPIO.LOW)

    def distanceInCM(self):

        try:
            self.initializeSensor()
            #cuando se inicializa el sensor pone el pulso echo en HIGH
            while True:
                startTime = time.time()
                if GPIO.input(self.ECHO) == GPIO.HIGH:
                    break

            #cuando recive el pulso el sensor pone el pin echo en LOW
            while True:
                endTime = time.time()
                if GPIO.input(self.ECHO) == GPIO.LOW:
                    break

            duration = endTime - startTime
            distancia = (conf.SOUND_SPEED * duration) / 2 #La distancia sera el tiempo que tarda el pulso * la velocidad entre 2 por que tenemos que medir la ida solo

            # Imprimimos resultado
        finally:
            return distancia
    def cleanUp(self):
        GPIO.cleanup()


