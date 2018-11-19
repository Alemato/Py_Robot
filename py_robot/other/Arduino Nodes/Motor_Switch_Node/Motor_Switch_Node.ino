// libreria ros
#include <ros.h>
// custom message Motor_Switch_Node
#include <py_robot/Motor_Switch_Node.h>
// custom message Controller_Node
#include <py_robot/Controller_To_Motor_Node.h>

// handle nodon ROS
ros::NodeHandle nh;

// assegnamento pin motori 1 e 2
#define SXPWM 3
#define SXIN1 4
#define SXIN2 5

// assegnamento pin motori 3 e 4
#define DXPWM 6
#define DXIN1 7
#define DXIN2 8


// assegnamento pin switch
#define switchFront 11
#define switchLeft 10
#define switchRight 9

// variabili globali
String comando;
int vel;

//funzione callback
// PARAM: messaggio ros velo

void callback( const py_robot::Controller_To_Motor_Node& velo) {
  // assegnamento del comando impartito dal Nodo Controller
  comando = velo.velo;

}
// funzione sottoscrizione di ros
ros::Subscriber<py_robot::Controller_To_Motor_Node> motor_sub("controller_To_Motor", callback);

// ros custom message sonar_volt
py_robot::Motor_Switch_Node switches;

// ros inizializzazione Pubblisher sonar_volt
ros::Publisher switch_pub("switches", &switches);

// funzione per switch
// PARAM: switchpin
// RETURN 0 se il lo switch non è attivato, 1 se è attivato

void setup() {
  // inizializzazione nodo
  nh.initNode();
  nh.advertise(switch_pub);
  nh.subscribe(motor_sub);

  // pin switch
  pinMode(switchFront, INPUT);
  pinMode(switchRight, INPUT);
  pinMode(switchLeft, INPUT);
  // pin motori 1 e 2 di sinistra
  pinMode(SXPWM, OUTPUT);
  pinMode(SXIN1, OUTPUT);
  pinMode(SXIN2, OUTPUT);
  analogWrite(SXPWM, 0);

  // pin motori 3 e 4 di destra
  pinMode(DXPWM, OUTPUT);
  pinMode(DXIN1, OUTPUT);
  pinMode(DXIN2, OUTPUT);
  analogWrite(DXPWM, 0);

  delay(1000);
}

// funzione per switch
// PARAM: switchpin
// RETURN 0 se il lo switch non è attivato, 1 se è attivato

long switchsensor(int switchpin) {
  // controllo se lo switch è stato premuto
  if (digitalRead(switchpin) == HIGH) {
    delay(20);
    // dopo 20 millisecondi controllo di nuovo se è ancora premuto per evitare errori
    if (digitalRead(switchpin) == HIGH) {
      // ritorna 0 se lo switch non è stato attivato
      return 0;
    }
  }
  // ritorna 1 se lo switch è stato attivato
  return 1;
}

// funzioni relative ai comandi da impartire ai motori

// funzione Avanti
// PARAM: intero vel: parametro velocità
// PARAM: intero tempo: parametro tempo di esecuzione
void vaiAvanti(int vel, int tempo) {
  // relativo al motor drive collegato ai motori del lato sinistro
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);
  // velocità lato sinistro
  analogWrite(SXPWM, vel);
  // relativo al motor drive collegato ai motori del lato destro
  digitalWrite(DXIN1, 1);
  digitalWrite(DXIN2, 0);
  // velocità lato destro
  analogWrite(DXPWM, vel);

  delay(tempo);
}

// funzione Indietro
// PARAM: intero vel: parametro velocità
// PARAM: intero tempo: parametro tempo di esecuzione
void vaiIndietro(int vel, int tempo) {
  // relativo al motor drive collegato ai motori del lato sinistro
  fermo(0);
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);
  // velocità lato sinistro
  analogWrite(SXPWM, vel);
  // relativo al motor drive collegato ai motori del lato destro
  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 1);
  // velocità lato destro
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo(0);
}

// funzione Sinistra
// PARAM: intero vel: parametro velocità
// PARAM: intero tempo: parametro tempo di esecuzione
void vaiDestra(int vel, int tempo) {
  // relativo al motor drive collegato ai motori del lato sinistro
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);
  // velocità lato sinistro
  analogWrite(SXPWM, vel);
  // relativo al motor drive collegato ai motori del lato destro
  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 1);
  // velocità lato destro
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo(0);
  comando = "s";
}

// funzione Destra
// PARAM: intero vel: parametro velocità
// PARAM: intero tempo: parametro tempo di esecuzione
void vaiSinistra(int vel, int tempo) {
  // relativo al motor drive collegato ai motori del lato sinistro
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);
  // velocità lato sinistro
  analogWrite(SXPWM, vel);
  // relativo al motor drive collegato ai motori del lato destro
  digitalWrite(DXIN1, 1);
  digitalWrite(DXIN2, 0);
  // velocità lato destro
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo(0);
  comando = "s";
}

// funzione Stop
// PARAM: intero vel: parametro velocità
// PARAM: intero tempo: parametro tempo di esecuzione
void fermo(int tempo) {
  // relativo al motor drive collegato ai motori del lato sinistro
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 0);
  // velocità lato sinistro
  analogWrite(SXPWM, 0);
  // relativo al motor drive collegato ai motori del lato destro
  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 0);
  // velocità lato destro
  analogWrite(DXPWM, 0);

  delay(tempo);
}


void loop() {

  //switch case con i varin casi possibili dei comandi ricevuti dal Nodo Controller
  switch (comando[0]) {

    case 'a': vaiAvanti(100, 50);
      break;

    case 'b': vaiAvanti(150, 50);
      break;

    case 'c': vaiAvanti(200, 50);
      break;

    case 'd': vaiAvanti(255, 50);
      break;

    case 'e': vaiIndietro(150, 50);
      break;

    case 'l': vaiSinistra(255, 200);
      break;

    case 'r': vaiDestra(255, 200);
      break;

    case 'f': vaiSinistra(255, 50);   // correzione sinistra
      break;

    case 'g': vaiDestra(255, 50);    // correzione destra
      break;

    case 'h': vaiSinistra(255, 2100);  // 360 antiorario
      break;

    case 'i': vaiDestra(255, 2100);   //360 orario
      break;

    case 'm': vaiSinistra(255, 800); // 90° a sinistra
      break;

    case 'n': vaiDestra(255, 800);   // 90° a destra
      break;

    case 'o': vaiSinistra(255, 1200); // 180° a sinistra
      break;

    case 'p': vaiDestra(255, 1200);   // 180° a destra
      break;



    case 's': fermo(0);
      break;

  }

  // assegnamento valore, 0 o 1, dello switch centrale nella prima posizione dell'array switches,
  // prima variabile del custom message Motor_Switch_Node
  switches.switches[0] = switchsensor(switchFront);
  // assegnamento valore, 0 o 1, dello switch Sinistra nella seconda posizione dell'array switches,
  // prima variabile del custom message Motor_Switch_Node
  switches.switches[1] = switchsensor(switchLeft);
  // assegnamento valore, 0 o 1, dello switch Destro nella terza posizione dell'array switches,
  // prima variabile del custom message Motor_Switch_Node
  switches.switches[2] = switchsensor(switchRight);
  // funzione Publish ROS
  switch_pub.publish(&switches);
  // procedura da attuare dopo che uno degli switch viene attivato
  if (switches.switches[0] == 0 || switches.switches[1] == 0 || switches.switches[2] == 0) {
    // stop
    fermo(0);
    // indietro per ___ secondi
    vaiIndietro(150, 2000);
  }
  // attesa eventi ROS
  nh.spinOnce();
  delay(10);
}
