#include <Servo.h>
#include <SoftwareSerial.h>
#include <ros.h>
#include <py_robot/Lidar_Compass_Node.h>
#include <py_robot/Controller_To_Lidar_Node.h>

// inizializzazione nodo ros
bool lidar = false;
ros::NodeHandle nh;

py_robot::Controller_To_Lidar_Node controller_node_msg;
py_robot::Lidar_Compass_Node lidar_compass_msg;
ros::Publisher pub_lidar_compass("lidar_compass_sub", &lidar_compass_msg);

// callback Subsciber
void callback(const py_robot::Controller_To_Lidar_Node& msg) {
  if (msg.on_off_lidar == true) {
    lidar = true;
  }
}

ros::Subscriber<py_robot::Controller_To_Lidar_Node> lidar_sub("controller_pub", callback);


// Assegnamento dei pin di collegamento e variabili

// Servo
#define servopin 2


// Lidar
#define lidarRX 3
#define lidarTX 4

// Compas
#define compassRX 6
#define compassTX 5

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

void setup() {
  nh.initNode();
  nh.advertise(pub_lidar_compass);
  nh.subscribe(lidar_sub);
  myservo.attach(servopin);
  Serial1.begin(115200);
  cmps11.begin(9600);
}

int bin_to_dec() {
  char input_binary_string[] = "111";
  int value = strtol(input_binary_string, NULL, 2);
}

void readcompass() {
  unsigned char high_byte, low_byte, angle8 ;
  unsigned int angle16;

  cmps11.write(CMPS_GET_ANGLE16);  // Request and read 16 bit angle
  while (cmps11.available() < 2);
  high_byte = cmps11.read();
  low_byte = cmps11.read();
  angle16 = high_byte;                // Calculate 16 bit angle
  angle16 <<= 8;
  angle16 += low_byte;
  lidar_compass_msg.angle16 = (int)angle16;
  
  cmps11.write(CMPS_GET_ANGLE8);  // Request and read 8 bit angle
  while (cmps11.available() < 1);
  lidar_compass_msg.angle8 = (int)cmps11.read();

  cmps11.write(CMPS_GET_PITCH);   // Request and read pitch value
  while (cmps11.available() < 1);
  lidar_compass_msg.pitch = (int)cmps11.read();

  cmps11.write(CMPS_GET_ROLL);         // Request and read roll value
  while (cmps11.available() < 1);
  lidar_compass_msg.roll = (int)cmps11.read();

  cmps11.write(CMPS_GET_MAG_RAW);    // Request and read mag value
  while (cmps11.available() < 6);
  lidar_compass_msg.mag[0] = (int)cmps11.read();
  lidar_compass_msg.mag[1] = (int)cmps11.read();
  lidar_compass_msg.mag[2] = (int)cmps11.read();
  lidar_compass_msg.mag[3] = (int)cmps11.read();
  lidar_compass_msg.mag[4] = (int)cmps11.read();
  lidar_compass_msg.mag[5] = (int)cmps11.read();

  cmps11.write(CMPS_GET_ACCEL_RAW);    // Request and read mag accel
  while (cmps11.available() < 6);
  lidar_compass_msg.acc[0] = (int)cmps11.read();
  lidar_compass_msg.acc[1] = (int)cmps11.read();
  lidar_compass_msg.acc[2] = (int)cmps11.read();
  lidar_compass_msg.acc[3] = (int)cmps11.read();
  lidar_compass_msg.acc[4] = (int)cmps11.read();
  lidar_compass_msg.acc[5] = (int)cmps11.read();

  cmps11.write(CMPS_GET_GYRO_RAW);    // Request and read mag gyro
  while (cmps11.available() < 6);
  lidar_compass_msg.gyro[0] = (int)cmps11.read();
  lidar_compass_msg.gyro[1] = (int)cmps11.read();
  lidar_compass_msg.gyro[2] = (int)cmps11.read();
  lidar_compass_msg.gyro[3] = (int)cmps11.read();
  lidar_compass_msg.gyro[4] = (int)cmps11.read();
  lidar_compass_msg.gyro[5] = (int)cmps11.read();

  cmps11.write(CMPS_GET_TEMP_RAW);    // Request and read mag temp
  while (cmps11.available() < 2);
  lidar_compass_msg.temp = (int)cmps11.read();
  lidar_compass_msg.temp = (int)cmps11.read();                                 //da rivedere
  
  delay(100);
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

int leggiservo() {
  int dist;
  for (int pos = 0; pos < 10; pos++) {
    myservo.write(pos);
    delay(15);                          // delay da testare
    dist = dist + readlidar2();

  }
  return dist;
}
void loop() {
  int arraydist[18];
  myservo.write(90);
  readcompass();
  if (lidar == true) {                 // variabile dal nodo controller
    myservo.write(0);
    delay(200);                           // delay da testare
    int appo = 0;
    for (int i = 0; i < 18; i++) {
      arraydist[i] = leggiservo() / 10;
    }
    for (int i = 0; i < 18; i++) {
      lidar_compass_msg.lidar[i] = arraydist[i];
    }
    lidar = false;
  }
  pub_lidar_compass.publish(&lidar_compass_msg);
  nh.spinOnce();
  delay(100);

}
