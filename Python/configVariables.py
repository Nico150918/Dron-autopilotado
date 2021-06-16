
#Variables configurables
SOUND_SPEED = 34300 #la velocidad del sonido en cm/s se puede configurar para que se ajuste mas precisamente a la disctancia real
DEFAULT_DATA_VALUE = "50, 50, 50, 0, 0, 0, 0, 0"

#Variables fijas
ENDVAL = 255               #Si queremos solo modificar solo los primeros canales podemos acortar la información a trasmitir
ERROR_CODE = 254            #Si se envia un valor mal reinicia el envio de la secuencia
EMERGENCY_DESCENT = 253    #En caso de error,un decenso controlado
EMERGENCY_ALT_DESCENT = 252 #En caso de error, apaga los motores y deja caer el dron
