import time,sys
from configVariables import ENDVAL,MAX_SPEED,ROLL,PITCH,ACEL, EMERGENCY_DESCENT,CLOSEST_DIST, ORDER,EMERGENCY_ALT_DESCENT
from multiprocessing import Process

class flight:

    def __init__(self,instructions, SPI):
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
        super(flightDistance, self).__init__(*args, **kwargs)

    def fly(self):
        for instruction in self.instrutions:
            distance = instruction["distance"]
            values = instruction["values"]

            if len(values) < 8 and values[len(values)-1] <= 100:
                values.add(ENDVAL)
                print("Añadiendo end val")
            self.SPI.sendData(values)
            duration = self.dirProportionClacSleep(values[ROLL],values[PITCH],values[ACEL],distance)
            print("Distance",distance,"m","Sleep", duration,"s")
            time.sleep(float(duration))

    def dirProportionClacSleep(self, roll, pitch, acel, dist):
        try:
            xAxysPower = abs(roll-50)/50
            yAxysPower = abs(pitch-50)/50
            power = acel/100
            print(xAxysPower,yAxysPower,power)
            estimatedSpeed = MAX_SPEED*(xAxysPower+yAxysPower)*power
            print("Velocidad estimada = ", estimatedSpeed)
            return dist/estimatedSpeed
        except:
            self.SPI.sendData([253])
            print("Comenzado aterrizaje ")
            time.sleep(0.5)
            exit(0)

    def __str__(self):
        print("Vuelo por distancias:\n instrucciones:",self.instrutions)

class flightDistanceLoop(flight):

    def __init__(self,times, *args, **kwargs):
        super(flightDistanceLoop, self).__init__(*args, **kwargs)
        self.times = times

    def fly(self):
        for i in range(1,self.times):
            for instruction in self.instrutions:
                distance = instruction["distance"]
                values = instruction["values"]
                if len(values) < 8 and values[len(values)-1] <= 100:
                    values.add(ENDVAL)
                    print("Añadiendo end val")
                self.SPI.sendData(values)
                duration = self.dirProportionClacSleep(values[ROLL],values[PITCH],values[ACEL],distance)
                print("Distance",distance,"m","Sleep", duration,"s")
                time.sleep(float(duration))

    def dirProportionClacSleep(self, roll, pitch, acel, dist):
        try:
            xAxysPower = abs(roll-50)/50
            yAxysPower = abs(pitch-50)/50
            print(xAxysPower,yAxysPower)
            power = acel/100
            estimatedSpeed = MAX_SPEED*(xAxysPower+yAxysPower)*power
            print("Velocidad estimada = ", estimatedSpeed)
            return dist/estimatedSpeed
        except:
            self.SPI.sendData([253])
            print("Comenzado aterrizaje ")
            time.sleep(0.5)
            exit(0)

    def __str__(self):
        print("Vuelo bucle distancia:\n instrucciones:", self.instrutions, "\n Times:", self.times)

class flightSensor(flight):
    def __init__(self, sensors, *args, **kwargs):
        super(flightSensor, self).__init__(*args, **kwargs)
        self.sensors = sensors

    def fly(self):
        for instruction in self.instrutions:
            distance = instruction["distance"]
            values = instruction["values"]
            if len(values) < 8 and values[len(values)-1] <= 100:
                values.add(ENDVAL)
                print("Añadiendo end val")
            self.SPI.sendData(values)
            duration = self.dirProportionClacSleep(values[ROLL],values[PITCH],values[ACEL],distance)
            print("Distance",distance,"m","Sleep", duration,"s")
            processDist = Process(target=self.checkDistance,args=(duration,[values],))
            processWait = Process(target=self.wait,args=(duration,))
            processDist.start()
            processWait.start()
            processDist.join()
            processWait.kill()
            processWait.join()
            print ("flight ended")

    def dirProportionClacSleep(self, roll, pitch, acel, dist):
        try:
            xAxysPower = abs(roll-50)/50
            yAxysPower = abs(pitch-50)/50
            print(xAxysPower,yAxysPower)
            power = acel/100
            estimatedSpeed = MAX_SPEED*(xAxysPower+yAxysPower)*power
            print("Velocidad estimada = ", estimatedSpeed)
            return dist/estimatedSpeed
        except:
            self.SPI.sendData([EMERGENCY_DESCENT])
            print("Comenzado aterrizaje ")
            time.sleep(0.5)
            exit(0)

    def wait(self,dur):
        time.sleep(dur)


    def checkDistance(self,duration,values):
        timeStart = time.time()
        cont = 0
        while time.time()-timeStart < duration:
            xAxysPower = abs(values[ROLL] - 50) / 50
            yAxysPower = abs(values[PITCH] - 50) / 50
            closestX = max(CLOSEST_DIST*xAxysPower, 20)
            closesty = max(CLOSEST_DIST*yAxysPower, 20)
            order = ORDER
            for sensor in self.sensors:
                direction = order.pop()
                dist = sensor.distanceInCM()
                if dist < 10:
                    self.SPI.sendData(EMERGENCY_ALT_DESCENT)
                if direction == "FRONT" or direction == "BACK":
                    if dist < closestX:
                        self.SPI.sendData([50,255])#Detiene el dron frontal, manteniendo el resto de movimiento
                        cont += 1
                if direction == "LEFT" or direction == "RIGHT":
                    if dist < closesty:
                        self.SPI.sendData([values[ROLL],50,255])#Detiene el dron lateral, manteniendo el resto de movimiento
                        cont += 1
                if direction == "TOP" or direction == "BOTTOM":
                    if dist < 30:
                        self.SPI.sendData([EMERGENCY_DESCENT])#Apaga el dron por que un obstaculo esta demasiado cerca
                if cont >= 2:
                    sys.exit()
            time.sleep(0.1)





    def __str__(self):
        print("Vuelo bucle distancia:\n instrucciones:", self.instrutions, "\n Times:", self.times)

