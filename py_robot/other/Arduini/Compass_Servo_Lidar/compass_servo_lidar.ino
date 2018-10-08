#include <Servo.h>
#include <SoftwareSerial.h>
// Assegnamento dei pin di collegamento e variabili

// Servo
#define servopin 2
int pos = 0;

// Lidar
#define lidarRX 3
#define lidarTX 4

int dist;// LiDAR actually measured distance value
int strength;// LiDAR signal strength
int check;// check numerical value storage
int i;
int uart[9];// store data measured by LiDAR
const int HEADER=0x59;// data package frame header

int arraydist[181];

// Compas
#define compassRX 6
#define compassTX 5
//#define CMPS11_ADDRESS 0x60  // Address of CMPS11 shifted right one bit for arduino wire library
//#define ANGLE_8  1           // Register to read 8bit angle from

#define CMPS_GET_ANGLE8 0x12
#define CMPS_GET_ANGLE16 0x13
#define CMPS_GET_PITCH 0x14
#define CMPS_GET_ROLL 0x15

unsigned char high_byte, low_byte, angle8;
char pitch, roll;
unsigned int angle16;

// Creazione oggetti

// Servo
Servo myservo;

// Lidar
SoftwareSerial Serial1(lidarRX, lidarTX);
SoftwareSerial cmps11 = SoftwareSerial(compassTX, compassRX);

void setup() {
  myservo.attach(servopin);
  Serial.begin(9600);
  Serial1.begin(115200);
  cmps11.begin(9600);
  //index=0;
  //distance=0;
  //strength=0;
}

uint8_t Checksum(uint8_t *data, uint8_t length){
  uint16_t  count;
  uint16_t  Sum = 0;
  for (count = 0; count < length; count++)
    Sum = Sum + data[count];
  return (Sum); 
 }



void readcompass(){
  cmps11.write(CMPS_GET_ANGLE16);  // Request and read 16 bit angle
  while(cmps11.available() < 2);
  high_byte = cmps11.read();
  low_byte = cmps11.read();
  angle16 = high_byte;                // Calculate 16 bit angle
  angle16 <<= 8;
  angle16 += low_byte;
  
  cmps11.write(CMPS_GET_ANGLE8);  // Request and read 8 bit angle
  while(cmps11.available() < 1);
  angle8 = cmps11.read();
  
  cmps11.write(CMPS_GET_PITCH);   // Request and read pitch value
  while(cmps11.available() < 1);
  pitch = cmps11.read();
  
  cmps11.write(CMPS_GET_ROLL);    // Request and read roll value
  while(cmps11.available() < 1);
  roll = cmps11.read();
  
  Serial.print("roll: ");            // Display roll data
  Serial.print(roll, DEC);
  
  Serial.print("    pitch: ");          // Display pitch data
  Serial.print(pitch, DEC);
  
  Serial.print("    angle full: ");       // Display 16 bit angle with decimal place
  Serial.print(angle16 / 10, DEC);
  Serial.print(".");
  Serial.print(angle16 % 10, DEC);
  
  Serial.print("    angle 8: ");        // Display 8bit angle
  Serial.println(angle8, DEC);
  
  delay(100);                           // Timeout 100ms
  
}

/* READ BINARY MODE LIDAR 
Send this command for pix format(ascii x.xx cr-lf) output is 42 57 02 00 00 00 04 06
Send this command for standard output is   42 57 02 00 00 00 01 06 

Standard output= 
Byte1-2   Byte3   Byte4   Byte5     Byte6     Byte7     Byte8    Byte9
0x59 59   Dist_L  Dist_H  Strength_L  Strength_H   Reserved   Raw.Qual  CheckSum_
*/



int readlidar2(){
  //check whether the serial port has data input
  if (Serial1.available()){
      // determine data package frame header 0x59
      if(Serial1.read()==HEADER){
        uart[0]=HEADER;
        //determine data package frame header 0x59
        if(Serial1.read()==HEADER){
           uart[1]=HEADER;
           // store data to array
           for(i=2;i<9;i++){
            uart[i]=Serial1.read();
            }
            // check the received data as per protocols
            check=uart[0]+uart[1]+uart[2]+uart[3]+uart[4]+uart[5]+uart[6]+uart[7];
            if(uart[8]==(check&0xff)){
              // calculate distance value
              dist=uart[2]+uart[3]*256;
              dist= dist-20;
              // calculate signal strength value
              strength=uart[4]+uart[5]*256;
              Serial.print("dist = ");
              // output LiDAR tests distance value
              Serial.print(dist);
              Serial.print('\t');
              Serial.print("strength = ");
              // output signal strength value
              Serial.print(strength);
              Serial.print('\n');
           }
       }
    }
  }
  return dist;
}
void loop() {
  Serial.println("parto");
  readcompass();
  Serial.println("dopo sonar");
  for (i=0; i<180; i++){
    myservo.write(i);
    delay(2);
    arraydist[i]=readlidar2();
    delay(2);
  }
  myservo.write(90);
  Serial.println("dopo lidar");
  for (i=0; i<180; i++){
    Serial.println(arraydist[i]);
  }
  delay(100);

}