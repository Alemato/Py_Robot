#include <Servo.h>
#include <SoftwareSerial.h>
#include <ros.h>
#include <py_robot/Lidar_Compass_Node_Arduino.h>
#include <py_robot/Controller_To_Lidar_Node.h>

// inizializzazione nodo ros
//bool lidar = false;
ros::NodeHandle nh;
py_robot::Controller_To_Lidar_Node controller_node_msg;
py_robot::Lidar_Compass_Node_Arduino lidar_compass_msg;
ros::Publisher pub_lidar_compass("lidar_compass_sub", &lidar_compass_msg);




// Assegnamento dei pin di collegamento e variabili

// Servo
#define servopin 2


// Lidar
#define lidarRX 3
#define lidarTX 4

//int dist;// LiDAR actually measured distance value
//int strength;// LiDAR signal strength
//int check;// check numerical value storage
//int i;
//int uart[9];// store data measured by LiDAR
//const int HEADER = 0x59; // data package frame header


// callback Subsciber
void callback(const py_robot::Controller_To_Lidar_Node& msg) {
  if (msg.on_off_lidar == true) {
    //lidar = true;
  }
}

// Compas
#define compassRX 6
#define compassTX 5

#define CMPS_GET_ANGLE8 0x12
#define CMPS_GET_ANGLE16 0x13
#define CMPS_GET_PITCH 0x14
#define CMPS_GET_ROLL 0x15

//unsigned char high_byte, low_byte, angle8;
//char pitch, roll;
//unsigned int angle16;

// Creazione oggetti

// Servo
Servo myservo;

// Lidar
SoftwareSerial Serial1(lidarRX, lidarTX);
SoftwareSerial cmps11 = SoftwareSerial(compassTX, compassRX);

void setup() {
  nh.initNode();
  nh.advertise(pub_lidar_compass);
  myservo.attach(servopin);
  Serial1.begin(115200);
  cmps11.begin(9600);
}

uint8_t Checksum(uint8_t *data, uint8_t length) {
  uint16_t  count;
  uint16_t  Sum = 0;
  for (count = 0; count < length; count++)
    Sum = Sum + data[count];
  return (Sum);
}


void readcompass() {
  unsigned char high_byte, low_byte, angle8;
  char pitch, roll;
  unsigned int angle16;


  cmps11.write(CMPS_GET_ANGLE16);  // Request and read 16 bit angle
  while (cmps11.available() < 2);
  high_byte = cmps11.read();
  low_byte = cmps11.read();
  angle16 = high_byte;                // Calculate 16 bit angle
  angle16 <<= 8;
  angle16 += low_byte;

  cmps11.write(CMPS_GET_ANGLE8);  // Request and read 8 bit angle
  while (cmps11.available() < 1);
  angle8 = cmps11.read();

  cmps11.write(CMPS_GET_PITCH);   // Request and read pitch value
  while (cmps11.available() < 1);
  pitch = cmps11.read();

  cmps11.write(CMPS_GET_ROLL);    // Request and read roll value
  while (cmps11.available() < 1);
  roll = cmps11.read();

  lidar_compass_msg.roll = roll;

  lidar_compass_msg.pitch = pitch;

  lidar_compass_msg.angle16 = angle16;

  lidar_compass_msg.angle8 = angle8;

  delay(100);                           // Timeout 100ms

}

int readlidar2() {
  int dist;
  int strength;
  int check;
  int uart[9];
  const int HEADER = 0x59; // data package frame header
  //check whether the serial port has data input
  if (Serial1.available()) {
    // determine data package frame header 0x59
    if (Serial1.read() == HEADER) {
      uart[0] = HEADER;
      //determine data package frame header 0x59
      if (Serial1.read() == HEADER) {
        uart[1] = HEADER;
        // store data to array
        for (int i = 2; i < 9; i++) {
          uart[i] = Serial1.read();
        }
        // check the received data as per protocols
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) {
          // calculate distance value
          dist = uart[2] + uart[3] * 256;
          dist = dist - 20;
          // calculate signal strength value
          strength = uart[4] + uart[5] * 256;
        }
      }
    }
  }
  return dist;
}
void loop() {
  int arraydist[181];
  bool lidar = false;
  myservo.write(90);
  readcompass();
  if (lidar == true) {                 // variabile dal nodo controller
    myservo.write(0);
    delay(1000);                           // delay da testare
    for (int pos = 0; pos < 180; pos++) {
      myservo.write(pos);
      delay(15);                          // delay da testare
      arraydist[pos] = readlidar2();
    }
    for (int i = 0; i < 180; i++) {
      lidar_compass_msg.lidar[i] = arraydist[i];
    }
    lidar = false;
  }
  pub_lidar_compass.publish(&lidar_compass_msg);
  nh.spinOnce();
  delay(100);

}
