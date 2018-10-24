// libreria ros
#include <ros.h>
// custom message Lidar_Compass_Node
#include <py_robot/Lidar_Compass_Node.h>
// custom message Controller_Node
#include <py_robot/Controller_To_Lidar_Node.h>
// libreria Servo Motore
#include <Servo.h>
// libreria seriale di comunicazione con il Lidar e del Compass
#include <SoftwareSerial.h>

// handle nodon ROS
ros::NodeHandle nh;

// assegnamento pin Servo Motore
#define servopin 2

// assegnamento pin Lidar
#define lidarRX 3
#define lidarTX 4

// assegnamento pin Compass
#define compassRX 6
#define compassTX 5

// assegnamento variabili per Compass
#define CMPS_GET_ANGLE8 0x12
#define CMPS_GET_ANGLE16 0x13
#define CMPS_GET_PITCH 0x14
#define CMPS_GET_ROLL 0x15
#define CMPS_GET_MAG_RAW 0x19
#define CMPS_GET_ACCEL_RAW 0x20
#define CMPS_GET_GYRO_RAW 0x21
#define CMPS_GET_TEMP_RAW 0x22


// Servo
Servo myservo;

// Lidar
SoftwareSerial Serial1(lidarRX, lidarTX);
SoftwareSerial cmps11 = SoftwareSerial(compassTX, compassRX);

// variabile globale per gestire l'attivazione del Lidar
bool lidar = false;

// funzone callback
// PARAM: messaggio ros msg

void callback(const py_robot::Controller_To_Lidar_Node& msg) {
  //controllo se il Nodo Controller ha inviato il comando per attivare il Lidar
  //tramite la variabile booleana "on_of_lidar"
  if (msg.on_off_lidar == true) {
    //setto la variabile globale "lidar" a true
    lidar = true;
  }
}

// funzione sottoscrizione di ROS
ros::Subscriber<py_robot::Controller_To_Lidar_Node> lidar_sub("controller_To_Lidar", callback);
// ROS custom message Lidar_Compass
py_robot::Lidar_Compass_Node lidar_compass_msg;

// ROS inizializzazione Pubblisher Lidar_Compass
ros::Publisher pub_lidar_compass("lidar_compass", &lidar_compass_msg);



void setup() {
  // ROS inizializzazione nodo
  nh.initNode();
  // ROS creazione Publisher
  nh.advertise(pub_lidar_compass);
  // Ros creazione Subscriber
  nh.subscribe(lidar_sub);
  // inizializzazione Servo
  myservo.attach(servopin);
  // inizializzazione seriale per il Lidar
  Serial1.begin(115200);
  // inizializzazione seriale per il Compass
  cmps11.begin(9600);
}

// funzione lettura Compass
// PARAM: CMPS_GET_ANGLE16, CMPS_GET_ANGLE8, CMPS_GET_PITCH, CMPS_GET_ROLL, CMPS_GET_MAG_RAW,  CMPS_GET_ACCEL_RAW, CMPS_GET_TEMP_RAW
// RETURN

void readcompass() {
  // variabili d'appoggio usate per calcolare gli angolazione a 8 bit e a 16 bit
  unsigned char high_byte, low_byte, angle8 ;
  unsigned int angle16;

  // richiesta e lettura dell'angolo a 16 bit
  cmps11.write(CMPS_GET_ANGLE16);
  while (cmps11.available() < 2);
  high_byte = cmps11.read();
  low_byte = cmps11.read();
  // calcolo dell'angolo a 16 bit
  angle16 = high_byte;
  angle16 <<= 8;
  angle16 += low_byte;
  //assegnamento dell'angolo calcolato nella variabile angle16 del custom message lidar_compass
  lidar_compass_msg.angle16 = (int)angle16;

  // richiesta e lettura dell'angolo a 8 bit
  cmps11.write(CMPS_GET_ANGLE8);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile angle8 del custom message lidar_compass
  lidar_compass_msg.angle8 = (int)cmps11.read();

  // richiesta e lettura del valore di beccheggio
  cmps11.write(CMPS_GET_PITCH);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile pitch del custom message lidar_compass
  lidar_compass_msg.pitch = (int)cmps11.read();

  //richiesta e lettura del valore di rollio
  cmps11.write(CMPS_GET_ROLL);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile roll del custom message lidar_compass
  lidar_compass_msg.roll = (int)cmps11.read();

  //richiesta e lettura dei valori del magnetometro
  cmps11.write(CMPS_GET_MAG_RAW);
  while (cmps11.available() < 6);
  //assegnamento dei valori 6 nella variabile array mag del custom message lidar_compass
  lidar_compass_msg.mag[0] = (int)cmps11.read();
  lidar_compass_msg.mag[1] = (int)cmps11.read();
  lidar_compass_msg.mag[2] = (int)cmps11.read();
  lidar_compass_msg.mag[3] = (int)cmps11.read();
  lidar_compass_msg.mag[4] = (int)cmps11.read();
  lidar_compass_msg.mag[5] = (int)cmps11.read();

  //richiesta e lettura dei valori dell'accelerometro
  cmps11.write(CMPS_GET_ACCEL_RAW);
  while (cmps11.available() < 6);
  //assegnamento dei 6 valori nella variabile array acc del custom message lidar_compass
  lidar_compass_msg.acc[0] = (int)cmps11.read();
  lidar_compass_msg.acc[1] = (int)cmps11.read();
  lidar_compass_msg.acc[2] = (int)cmps11.read();
  lidar_compass_msg.acc[3] = (int)cmps11.read();
  lidar_compass_msg.acc[4] = (int)cmps11.read();
  lidar_compass_msg.acc[5] = (int)cmps11.read();

  //richiesta e lettura dei valori del giroscopio
  cmps11.write(CMPS_GET_GYRO_RAW);
  while (cmps11.available() < 6)
    //assegnamento dei 6 valori nella variabile array gyro del custom message lidar_compass;
    lidar_compass_msg.gyro[0] = (int)cmps11.read();
  lidar_compass_msg.gyro[1] = (int)cmps11.read();
  lidar_compass_msg.gyro[2] = (int)cmps11.read();
  lidar_compass_msg.gyro[3] = (int)cmps11.read();
  lidar_compass_msg.gyro[4] = (int)cmps11.read();
  lidar_compass_msg.gyro[5] = (int)cmps11.read();

  //richiesta e lettura dei valori del termometro
  cmps11.write(CMPS_GET_TEMP_RAW);
  while (cmps11.available() < 2);
  //assegnamento dei 2 valori nella variabile array temp del custom message lidar_compass;
  lidar_compass_msg.temp = (int)cmps11.read();
  lidar_compass_msg.temp = (int)cmps11.read();

  delay(100);
}

// funzione lettura Lidar
// PARAM:
// RETURN: dist: distanza rilevata e calcolata

int readlidar() {
  int dist;
  int strength;
  int check;
  int uart[9];
  // frame di pacchetto dati dal Lidar
  const int HEADER = 0x59;
  //controllo se la porta seriale è disponibile
  if (Serial1.available()) {
    // determino il frame del pacchetto dati ell'header 0X59
    if (Serial1.read() == HEADER) {
      uart[0] = HEADER;
      // determino il frame del pacchetto dati ell'header 0X59
      if (Serial1.read() == HEADER) {
        uart[1] = HEADER;
        // salvo i dati letti dalla seriale in un array
        for (int i = 2; i < 9; i++) {
          uart[i] = Serial1.read();
        }
        // controllo i dati ricevuti in base ai protocolli
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) {
          // calcolo il valore della distanza
          dist = uart[2] + uart[3] * 256;
          dist = dist - 20;
          // calcolo il valore della forza del segnale
          strength = uart[4] + uart[5] * 256;
        }
      }
    }
  }
  // ritorno la distanza
  return dist;
}

// funzione Servo. Si occupa dello spostamento del servo che permette al lidar di leggere la distanza nei 180 gradi di fronte al rover
// dividendola in porzioni di 10 gradi ciascuna
// PARAM:
// RETURN: dist: array di dimensione 10 della porzione ca

int readservo() {
  int dist = 0;
  // ciclo che scorre i 10 gradi della porzione di spazio
  for (int pos = 0; pos < 10; pos++) {
    // setto la posizione del servo
    myservo.write(pos);
    delay(15);
    // somma delle distanze della porzione
    dist = dist + readlidar();
  }
  //ritorno la distanza 
  return dist;
}

void loop() {
  // variabile array nella quale salvo le medie delle 18 porzioni
  int arraydist[18];
  // calcolo i valori del Compass
  readcompass();
  // vedo se il Nodo Controller ha richiesto l'uso del lidar
  if (lidar == true) {
    // setto il servo in posizione 0                  
    myservo.write(0);
    delay(200);
    // ciclo che calcola la media delle 18 porzioni con il Servo ed il Lidar
    for (int i = 0; i < 18; i++) {
      arraydist[i] = readservo() / 10;
    }
    // store delle medie delle distanze nella variabile array lidar del custom message lidar_compass
    for (int i = 0; i < 18; i++) {
      lidar_compass_msg.lidar[i] = arraydist[i];
    }
    // reimposto la variabile lidar a false per il prossimo utilizzo
    lidar = false;
    // setto il servo in posizione centrale
    myservo.write(90);
  }
  // funzione Publish ROS 
  pub_lidar_compass.publish(&lidar_compass_msg);
  // attesa eventi ROS 
  nh.spinOnce();
  delay(10);
}
