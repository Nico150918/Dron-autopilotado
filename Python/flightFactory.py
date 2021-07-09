import flights
class FlightFactory:

    def createFlight(self, fp,SPI,sensorList):
        type = fp.getVal("type")
        if type == "default":
            return flights.flight(fp.getVal("instructions"),SPI,sensorList)
        if type == "loop":
            return flights.flightLoop(fp.getVal("times"),fp.getVal("instructions"),SPI,sensorList)
        if type == "distance":
            return flights.flightDistace(fp.getVal("instructions"),SPI,sensorList)
