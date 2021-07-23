#Variables configurables
SOUND_SPEED = 34300 #la velocidad del sonido en cm/s se puede configurar para que se ajuste mas precisamente a la disctancia real
DEFAULT_DATA_VALUE = "50, 50, 50, 0, 0, 0, 0, 0"
CLOSEST_DIST = 50 #como mucho a 50 cm frena
ORDER = ["FRONT","LEFT","RIGHT","BACK"] #Orden de los sensores, si tienes mas sensores añadir a la lista
TIPOS_DE_VUELO_IMPLEMENTADO = ["default","loop","distance","distanceLoop","distanceSensor"]#el identificador de cada tipo de vuelo

#Las posiciones del array de la velocidad
ROLL = 0
PITCH = 1
YAW = 2
ACEL = 3

#a que pines de la raspberry esta conectado
DEF_SPI_MODULE = 0
DEF_SPI_DISP = 0

MAX_SPI_HZ = 1000000 # Hz de la comunicación dependen de que placas utilices
SEC_DIST_CM = 100 # La distancia en cm para frenar

MAX_SPEED = 3 #m/s Esta velocidad es para las simualciones con la libreria MAVProxy se puede leer la velocidad del dron real
YAW_SPEED = 2 #segundos por vuelta, datos obtenidos de un dron (tambien se puede obtener con MAVproxy pero no fuenciona en simulaciones)

#Variables fijas
ENDVAL = 255               #Si queremos solo modificar solo los primeros canales podemos acortar la información a trasmitir
ERROR_CODE = 254            #Si se envia un valor mal reinicia el envio de la secuencia
EMERGENCY_DESCENT = 253    #En caso de error,un decenso controlado
EMERGENCY_ALT_DESCENT = 252 #En caso de error, apaga los motores y deja caer el dron
