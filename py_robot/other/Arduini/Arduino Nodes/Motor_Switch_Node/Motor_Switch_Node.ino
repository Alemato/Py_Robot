// libreria ros
#include <ros.h>
// custom message Motor_Switch_Node
#include <py_robot/Motor_Switch_Node.h>
// custom message Controller_Node
#include <py_robot/Controller_To_Motor_Node.h>
// libreria motor driver
#include <L298N.h>

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

// definizioni delle funzioni legate ai due motor driver che gestiscono
// rispettivamente i due motori di sinistra e due di destra
L298N sinistra(PWMA, AIN1, AIN2, AIN1, AIN2, PWMA);
L298N destra(PWMB, BIN1, BIN2, BIN1, BIN2, PWMB);

// variabili globali
String velocita;
char cmd[1];
int vel;
//int time_delay = 2000;

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

// funzione Avanti
// PARAM: intero vel: parametro velocità
void VaiAvanti(int vel, int time_delay) {
  // relativo al lato sinistro
  sinistra.forward(vel, time_delay);
  // relativo al lato destro
  destra.forward(vel, time_delay);

}
// funzione Indietro
// PARAM: intero vel: parametro velocità
void VaiIndietro(int vel, int time_delay) {
  // relativo al motor drive collegato ai motori del lato sinistro con velocità ___ e tempo ___
  sinistra.backward(vel, time_delay);
  // relativo al motor drive collegato ai motori del lato destro con velocità ___ e tempo ___
  destra.backward(vel, time_delay);
}

// funzione Sinistra
void VaiSinistra() {
  // relativo al motor drive collegato ai motori del lato sinistro con velocità ___ e tempo ___
  sinistra.backward(100, 2000);
  // relativo al motor drive collegato ai motori del lato destro con velocità ___ e tempo ___
  destra.forward(100, 2000);
}

// funzione Destra
void VaiDestra() {
  // relativo al motor drive collegato ai motori del lato sinistro con velocità ___ e tempo ___
  sinistra.forward(100, 2000);
  // relativo al motor drive collegato ai motori del lato destro con velocità ___ e tempo ___
  destra.backward(100, 2000);
}

// funzione Correzione a sinistra
void CorrezioneDestra() {
  // relativo al motor drive collegato ai motori del lato sinistro con velocità ___ e tempo ___
  sinistra.forward(100, 2000);
  // relativo al motor drive collegato ai motori del lato destro con velocità ___ e tempo ___
  destra.backward(100, 2000);
}

// funzione Correzione a destra
void CorrezioneSinistra() {
  // relativo al motor drive collegato ai motori del lato sinistro con velocità ___ e tempo ___
  sinistra.forward(100, 2000);
  // relativo al motor drive collegato ai motori del lato destro con velocità ___ e tempo ___
  destra.backward(100, 2000);
}

void loop() {

  //switch case con i varin casi possibili dei comandi ricevuti dal Nodo Controller
  switch (cmd[0]) {

    case 'a': VaiAvanti(70, 2000);
      break;

    case 'b': VaiAvanti(90, 2000);
      break;

    case 'c': VaiAvanti(110, 2000);
      break;

    case 'd': VaiAvanti(130, 2000);
      break;

    case 'e': VaiAvanti(150, 2000);
      break;

    case 'f': VaiAvanti(170, 2000);
      break;

    case 'g': VaiAvanti(190, 2000);
      break;

    case 'h': VaiAvanti(210, 2000);
      break;

    case 'i': VaiIndietro(80, 2000);
      break;

    case 'l': VaiIndietro(100, 2000);
      break;

    case 'm': VaiIndietro(150, 2000);
      break;

    case 'o': VaiIndietro(180, 2000);
      break;

    case 'p': VaiIndietro(210, 2000);
      break;

    case 'q': VaiSinistra();
      break;

    case 'r': VaiDestra();
      break;

    case 's': VaiAvanti(0, 2000);
      break;

    case 't': CorrezioneSinistra();
      break;

    case 'u': CorrezioneDestra();
      break;

    case 'v': VaiAvanti(0, 2000);    //stop per attivazione lidar
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
  if(switches.switches[0] == 0 || switches.switches[1] == 0 || switches.switches[2] == 0){
    // stop
    VaiAvanti(0, 2000);
    // indietro per ___ secondi
    VaiIndietro(80, 2000);
  }
  // attesa eventi ROS 
  nh.spinOnce();
  delay(10);
}

