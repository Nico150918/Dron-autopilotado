import RPi.GPIO as GPIO
import spidev
import time
from configVariables import ENDVAL,ERROR_CODE,EMERGENCY_DESCENT,EMERGENCY_ALT_DESCENT

class SPITransmiter:
    def __init__(self, module = 0, disp = 0, maxHz = 1000):
        GPIO.setmode(GPIO.BCM)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Abrimos el puerto SPI
        self.spi.max_speed_hz = 1000000  #Establecemos la velocidad máxima

        self.prevRet = 10
        self.sended = self.prevRet
        self.firstData = True

    def sendData(self,data):
        global sendedNoErr
        try:
            sendedNoErr = True
            i = 0
            for each in data:
                self.prevRet = self.spi.xfer([each])
                print("Sending =", each,"Last Sended =",self.sended, "Reciving =",self.prevRet[0])
                if self.prevRet[0] != self.sended and not self.firstData:
                    self.sendError(ERROR_CODE)
                    sendedNoErr = False
                    break
                self.sended = each
                self.firstData = False
                i += 1
                time.sleep(0.01)
        except KeyboardInterrupt:
            # Ctrl+C
            print("Interrupción por teclado")

        finally:
            return sendedNoErr

    def sendError(self,err = ERROR_CODE):
        print("error")
        self.spi.xfer([err])
        time.sleep(0.25)
        self.spi.xfer([EMERGENCY_DESCENT])
        time.sleep(0.25)
        self.sended = EMERGENCY_DESCENT

    def cleanUp(self):
        self.spi.close()
        GPIO.cleanup()
        print("GPIO.cleanup() y spi.close() ejecutados ")



