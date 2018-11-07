// libreria ros
#include <ros.h>
// custom message Compass_Node
#include <py_robot/Compass_Node.h>

// libreria seriale di comunicazione con il Compass
#include <SoftwareSerial.h>

// handle nodon ROS
ros::NodeHandle nh;

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

// Compass
SoftwareSerial cmps11 = SoftwareSerial(compassTX, compassRX);

// ROS custom message Compass
py_robot::Compass_Node compass_msg;

// ROS inizializzazione Pubblisher Compass
ros::Publisher pub_compass("compass", &compass_msg);

void setup() {
  // ROS inizializzazione nodo
  nh.initNode();
  // ROS creazione Publisher
  nh.advertise(pub_compass);
  // inizializzazione seriale per il Compass
  cmps11.begin(9600);
}

// funzione lettura Compass
// PARAM: CMPS_GET_ANGLE16, CMPS_GET_ANGLE8, CMPS_GET_PITCH, CMPS_GET_ROLL, CMPS_GET_MAG_RAW,  CMPS_GET_ACCEL_RAW, CMPS_GET_TEMP_RAW
// RETURN

void readcompass() {
  // variabili d'appoggio usate per calcolare gli angolazione a 8 bit e a 16 bit
  unsigned char high_byte, low_byte;
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
  //assegnamento dell'angolo calcolato nella variabile angle16 del custom message compass
  compass_msg.angle16 = (int)angle16;

  // richiesta e lettura dell'angolo a 8 bit
  cmps11.write(CMPS_GET_ANGLE8);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile angle8 del custom message compass
  compass_msg.angle8 = (int)cmps11.read();

  // richiesta e lettura del valore di beccheggio
  cmps11.write(CMPS_GET_PITCH);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile pitch del custom message compass
  compass_msg.pitch = (int)cmps11.read();

  //richiesta e lettura del valore di rollio
  cmps11.write(CMPS_GET_ROLL);
  while (cmps11.available() < 1);
  //assegnamento del valore nella variabile roll del custom message compass
  compass_msg.roll = (int)cmps11.read();
}

void loop() {
  readcompass();
  // funzione Publish ROS 
  pub_compass.publish(&compass_msg);
  // attesa eventi ROS 
  nh.spinOnce();
  delay(10);
}
