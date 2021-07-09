import flights
class FlightFactory:

    def createFlight(self, fp,SPI,sensorList):
        type = fp.getVal("type")
        if type == "default":
            return flights.flight(fp.getVal("instructions"), SPI,)
        if type == "loop":
            return flights.flightLoop(fp.getVal("times"), fp.getVal("instructions"), SPI)
        if type == "distance":
            return flights.flightDistance(fp.getVal("instructions"), SPI)
        if type == "distanceLoop":
            return flights.flightDistanceLoop(fp.getVal("instructions"), SPI)
