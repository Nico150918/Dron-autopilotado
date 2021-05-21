/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>
//valores de configuración
const int VAL_MIN_PWM = 35; //este es el valor mas bajo que puede leer mi controlador de vuelo
const int VAL_MAX_PWM = 150;//este es el valor mas alto que puede leer mi controlador de vuelo
const int NUM_CHANNELS = 8; //numero de canales que utilizas.

Servo roll, pitch, yaw, acel, aux1, aux2, aux3, aux4; //definimos los servos, en caso de que tu dron utilize mas de 8 añade aqui los canales que falten
Servo servos[NUM_CHANNELS] = {roll, pitch, yaw, acel, aux1, aux2, aux3, aux4};  //lista de servos, para facilitar la ampliación, en caso de que tu dron utilize mas de 8 añade aqui los canales que falten
int pins[NUM_CHANNELS] = {A0,A1,A3,A2,A4,A5,9,10};//Pines a los que va conectado cada puerto, ajustar a el diseño de cada dron correspondiente
int defaultValues[NUM_CHANNELS] = {50,50,50,0,0,0,0,0}; //Los porcentajes de potencia en los que quieres que se inicie el programa, añade los que falten y modifica para que se ajusten a tus necesidades

/*
 * Roll = inclinación lateral -> A0
 * pitch = inclinación Frontal -> A1
 * acel = aceleracion -> A3
 * yaw = rotación sobre su eje -> A2
 * 
 */
String updateLine;

struct arrayAcciones
   {  
    int arr[NUM_CHANNELS];
    byte ultimaPos;
   } ;
   
arrayAcciones process(String text);
int mapper(int value);

void setup() {
  for (int i = 0; i< NUM_CHANNELS; i++){
    servos[i].attach(pins[i]);
    servos[i].write(mapper(defaultValues[i])); 
  }
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()){
      updateLine = Serial.readString();
      arrayAcciones acciones =process(updateLine);
      for(int i = 0; i < acciones.ultimaPos; i++){
          servos[i].write(mapper(acciones.arr[i]));
          Serial.println(mapper(acciones.arr[i]));
        } 
    }
}


int mapper(int value){
  float proportion = (VAL_MAX_PWM-VAL_MIN_PWM)/100.0;
  return round(VAL_MIN_PWM + (float(value) *proportion));  
  }

arrayAcciones process(String text){
    int actVal = 0;
    byte pos = 0;
    int arr[NUM_CHANNELS];
      
    int len = text.length();
    for(int i = 0; i < len; i++){
      char act = text[i];
       if(act == ','||act == ']'){
        arr[pos] = actVal;
        pos++;
        actVal = 0;
      }else{
        actVal = String(act).toInt()+actVal*10;
      }
    }
    arrayAcciones res;
    res.ultimaPos = pos;
     for(int i = 0; i < pos; i++){
      res.arr[i] = arr[i];
    }
    return res;
  }
