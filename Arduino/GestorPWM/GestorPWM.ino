#include <Servo.h>
#include <pins_arduino.h>


//Valores configurables
const int VAL_MIN_PWM = 35; //este es el valor mas bajo que puede leer mi controlador de vuelo
const int VAL_MAX_PWM = 150;//este es el valor mas alto que puede leer mi controlador de vuelo
const int NUM_CHANNELS = 8; //numero de canales que utilizas.
int DEFAULT_VALUES[NUM_CHANNELS] = {50, 50, 50, 0, 0, 0, 0, 0};             //Los porcentajes de potencia en los que quieres que se inicie el programa, añade los que falten y modifica para que se ajusten a tus necesidades
int CONTROLED_DESCENT_VALUES[NUM_CHANNELS] = {50, 50, 50, 20, 0, 0, 0, 0};  //Los porcentajes de potencia en los que quieres que se descienda en caso de parada de emergencia
int ALT_DESCENT_VALUES[NUM_CHANNELS] = {50, 50, 50, 0, 0, 0, 0, 0};         //parada 100 total para emergencias

Servo roll, pitch, yaw, acel, aux1, aux2, aux3, aux4;                          //definimos los servos, en caso de que tu dron utilize mas de 8 añade aqui los canales que falten
Servo servos[NUM_CHANNELS] = {roll, pitch, yaw, acel, aux1, aux2, aux3, aux4}; //lista de servos, para facilitar la ampliación, en caso de que tu dron utilize mas de 8 añade aqui los canales que falten
int pins[NUM_CHANNELS] = {A0, A1, A3, A2, A4, A5, 9, 10};                      //Pines a los que va conectado cada puerto, ajustar a el diseño de cada dron correspondiente
int updateValues[NUM_CHANNELS];


///No modificar

byte sendedCont = 0;
volatile boolean intervalEnded;
bool lastError = false; 

const byte ENDVAL = 0b11111111;                //Si queremos solo modificar solo los primeros canales podemos acortar la información a trasmitir
const byte ERROR_CODE = 0b11111110;            //Si se envia un valor mal reinicia el envio de la secuencia
const byte EMERGENCY_DESCENT = 0b11111101;     //En caso de error,un decenso controlado
const byte EMERGENCY_ALT_DESCENT = 0b11111100; //En caso de error, apaga los motores y deja caer el dron




/*
 * Roll = inclinación lateral -> A0
 * pitch = inclinación Frontal -> A1
 * acel = aceleracion -> A3
* yaw = rotación sobre su eje -> A2
 * 
 */

struct arrayAcciones
{
    int arr[NUM_CHANNELS];
    byte ultimaPos;
};

arrayAcciones process(int values[]);
int mapper(int value);
boolean manageSPIInput(byte input);

void setup()
{
    for (int i = 0; i < NUM_CHANNELS; i++)
    {
        servos[i].attach(pins[i]);
        servos[i].write(mapper(DEFAULT_VALUES[i]));
    }
    intialiceSPISlave();
    Serial.begin(115200);
    Serial.println("Inicinado Ejecucion");
}

void loop()
{
    if (intervalEnded)
    {
        arrayAcciones acciones = process();
        Serial.println(acciones.ultimaPos);
        for (int i = 0; i < NUM_CHANNELS; i++)
        {
            servos[i].write(mapper(acciones.arr[i]));
            Serial.print(acciones.arr[i]);Serial.print(" = ");Serial.println(mapper(acciones.arr[i]));
        }
        sendedCont = 0;
        intervalEnded = false;
    }
}

void intialiceSPISlave()
{
    pinMode(MISO, OUTPUT);
    //Activa el slave mode
    SPCR |= _BV(SPE);
    //Permite las interrupciones
    SPCR |= _BV(SPIE);
    sendedCont = 0;
    intervalEnded = false;
} // end of setup

int mapper(int value)
{
    float proportion = (VAL_MAX_PWM - VAL_MIN_PWM) / 100.0;
    return round(VAL_MIN_PWM + (float(value) * proportion));
}

arrayAcciones process()
{
    arrayAcciones res;
    res.ultimaPos = sendedCont;
    for (int i = 0; i < sendedCont; i++)
    {
        res.arr[i] = updateValues[i];
        Serial.print(updateValues[i]);Serial.print(" -> ");Serial.println(res.arr[i]);
    }
    sendedCont = 0;
    return res;
}

// SPI interrupt
ISR(SPI_STC_vect)
{
    byte input = SPDR;

    if (sendedCont == NUM_CHANNELS - 1)
    {
        intervalEnded = true;        
    } 
    lastError = manageSPIInput(input); 
}

boolean manageSPIInput(byte input)
{
    boolean ret = false;
    //Serial.println(input);
    switch (input)
    {
    case ERROR_CODE:
        Serial.println("Error code");
        sendedCont = 0;        
        ret = true;
        break;

    case EMERGENCY_DESCENT:
        Serial.println("EMERGENCY_DESCENT code");
        for (int i = 0; i < NUM_CHANNELS; i++){
            updateValues[i] = CONTROLED_DESCENT_VALUES[i];
        }
        sendedCont = NUM_CHANNELS-1; 
        intervalEnded = true; 
        ret = true;
        break;

    case EMERGENCY_ALT_DESCENT:
        Serial.println("EMERGENCY_ALT_DESCENT code");
        for (int i = 0; i < NUM_CHANNELS; i++){
            updateValues[i] = ALT_DESCENT_VALUES[i];
        }
        sendedCont = NUM_CHANNELS-1; 
        intervalEnded = true; 
        ret = true;
        break;

    case ENDVAL:
        intervalEnded = true;
        for (size_t i = sendedCont-1; i < NUM_CHANNELS; i++)
        {
            updateValues[sendedCont] = 0;
        }
        break;

    default:
        updateValues[sendedCont] = input;
        sendedCont++;
        break;
    }
    return ret;
}