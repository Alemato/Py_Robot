// libreria ros
#include <ros.h>
// custom message Sonar_Volt_Node
#include <py_robot/Sonar_Volt_Node.h>

// ros
ros::NodeHandle nh;

// assegnamento dei pin sonar
#define echoPinFront 2
#define trigPinFront 3
#define echoPinRight 4
#define trigPinRight 5
#define echoPinLeft 6
#define trigPinLeft 7

// assegnamento pin voltometer
#define analogInput 0

// variabili voltometer
float val;
float temp;

// ros custom message sonar_volt
py_robot::Sonar_Volt_Node sonar_volt_msg;

// ros inizializzazione Pubblisher sonar_volt
ros::Publisher sonar_volt_pub("sonar_volt", &sonar_volt_msg);


void setup() {
  // inizializzazione nodo
  nh.initNode();
  nh.advertise(sonar_volt_pub);

  // pin sonar
  pinMode(echoPinFront, INPUT );
  pinMode(trigPinFront, OUTPUT );
  pinMode(echoPinRight, INPUT );
  pinMode(trigPinRight, OUTPUT );
  pinMode(echoPinLeft, INPUT );
  pinMode(trigPinLeft, OUTPUT );

  // pin voltometer
  pinMode(analogInput, INPUT);

}

// funzione per il sonar
// PARAM: triggerPin, echoPin
// RETURN: distance di tipo long, ritorna la lettura della distanza

long sonarsensor(int triggerPin, int echoPin) {
  long distance = 0;
  // spengo il trigger
  digitalWrite(triggerPin, LOW);
  // accendo il trigger
  digitalWrite(triggerPin, HIGH);
  // aspetto 10 millisecondi
  delayMicroseconds(10);
  // spengo il trigger
  digitalWrite(triggerPin, LOW);
  // tempo ritorno dell'impulso
  long times = pulseIn(echoPin, HIGH);
  // se il tempo non supera 38000 abbiamo perso l'impulso e ritornerà 0
  if (times < 38000) {
    // calcolo della distanza
    distance = 0.034 * times / 2;
    // ritorno la distanza
    return distance;
  }
  // ritorno la distanza = 0
  return distance;
}

// funzione voltometer
// RETURN: val di tipo float, ritorna voltaggio in imput dalla batteria

float voltometer() {
  // lettura segnale
    val=analogRead(0);
    // operazione di conversione segnale imput in volt
    temp=val/40.92;
    // sottraggo margine di errore 
    val=temp - 0.7;
    // ritorno valore volt
    return val;
}

void loop() {
  // assegnamento valore del sonar centrale nella prima posizione dell'array sonar, 
  // prima variabile del custom message Sonar_Volt  
  sonar_volt_msg.sonar[0] = sonarsensor(trigPinFront, echoPinFront);
  // assegnamento valore del sonar destro nella seconda posizione dell'array sonar, 
  // prima variabile del custom message Sonar_Volt 
  sonar_volt_msg.sonar[1] = sonarsensor(trigPinRight, echoPinRight);
  // assegnamento valore del sonar sinistro nella terza posizione dell'array sonar, 
  // prima variabile del custom message Sonar_Volt 
  sonar_volt_msg.sonar[2] = sonarsensor(trigPinLeft, echoPinLeft);
  // funzione del voltometro e assegnamento nella seconda variabile del custom message
  sonar_volt_msg.volt = voltometer();
  // funzione Publish ros 
  sonar_volt_pub.publish(&sonar_volt_msg);
  // attesa eventi ROS 
  nh.spinOnce();
  delay(10);
}
