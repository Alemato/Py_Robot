// libreria ros
#include <ros.h>
// custom message Motor_Switch_Node
#include <py_robot/Motor_Switch_Node.h>
// custom message Controller_Node
#include <py_robot/Controller_To_Motor_Node.h>

// handle nodon ROS
ros::NodeHandle nh;

// assegnamento pin motori 1 e 2
#define AIN1 2
#define AIN2 4
#define PWMA 3

// assegnamento pin motori 3 e 4
#define BIN1 5
#define BIN2 7
#define PWMB 6

// assegnamento pin switch
#define switchFront 8
#define switchLeft 9
#define switchRight 10

// variabili globali
char cmd[1];
int vel;

//funzione callback
// PARAM: messaggio ros velo

void callback( const py_robot::Controller_To_Motor_Node& velo) {
  // assegnamento del comando impartito dal Nodo Controller
  velocita = velo.velo;
  // conversione della da stringa ad array di char
  velocita.toCharArray(cmd, 1);

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

long switchsensor(int switchpin) {
  // controllo se lo switch è stato premuto
  if (digitalRead(switchpin) == HIGH) {
    delay(20);
    // dopo 20 millisecondi controllo di nuovo se è ancora premuto per evitare errori
    if (digitalRead(switchpin) == HIGH) {
      // procedura da attuare dopo che uno degli switch viene attivato
      // stop
      // VaiAvanti(0, 2000);
      // indietro per ___ secondi
      // VaiIndietro(80, 2000);
      // ritorna 0 se lo switch non è stato attivato
      return 0;
    }
  }
  // ritorna 1 se lo switch è stato attivato
  return 1;
}

// funzioni relative ai comandi da impartire ai motori

void vaiAvanti(int vel, int tempo) {
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1. 1);
  digitalWrite(DXIN2. 0);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
}

void vaiIndietro(int vel, int tempo) {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);

  digitalWrite(DXIN1. 0);
  digitalWrite(DXIN2. 1);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
}

void vaiSinistra(int vel, int tempo) {
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1. 0);
  digitalWrite(DXIN2. 1);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
}

void vaiDestra(int vel, int tempo) {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);

  digitalWrite(DXIN1. 1);
  digitalWrite(DXIN2. 0);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
}

void fermo() {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1. 0);
  digitalWrite(DXIN2. 0);

  analogWrite(SXPWM, 0);
  analogWrite(DXPWM, 0);
}

void setup() {
  // inizializzazione nodo
  nh.initNode();
  nh.advertise(switch_pub);
  nh.subscribe(motor_sub);

  //pin switch
  pinMode(switchFront, INPUT);
  pinMode(switchRight, INPUT);
  pinMode(switchLeft, INPUT);
}

void loop() {

  //switch case con i varin casi possibili dei comandi ricevuti dal Nodo Controller
  switch (cmd[0]) {

    case 'a': vaiAvanti(70, 2000);
      break;

    case 'b': vaiAvanti(90, 2000);
      break;

    case 'c': vaiAvanti(110, 2000);
      break;

    case 'd': vaiAvanti(130, 2000);
      break;

    case 'e': vaiAvanti(150, 2000);
      break;

    case 'f': vaiAvanti(170, 2000);
      break;

    case 'g': vaiAvanti(190, 2000);
      break;

    case 'h': vaiAvanti(210, 2000);
      break;

    case 'i': vaiIndietro(80, 2000);
      break;

    case 'l': vaiIndietro(100, 2000);
      break;

    case 'm': vaiIndietro(150, 2000);
      break;

    case 'o': vaiIndietro(180, 2000);
      break;

    case 'p': vaiIndietro(210, 2000);
      break;

    case 'q': vaiSinistra();
      break;

    case 'r': vaiDestra();
      break;

    case 's': fermo();
      break;

    case 't': vaiSinistra(100, 500);        \\ correzione a sinistra
      break;

    case 'u': vaiDestra(100, 500);          \\ correzione a destra
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
    VaiAvanti(0, 2000);
    // indietro per ___ secondi
    VaiIndietro(80, 2000);
  }
  // attesa eventi ROS
  nh.spinOnce();
  delay(10);
}

