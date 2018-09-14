#include <ros.h>
#include <ArduinoHardware.h>
#include <py_robot/Senso.h>

/* ros part*/
ros::NodeHandle nh;
py_robot::Senso senso;
ros::Publisher sensors_pub("senso", &senso);
/* end ros part*/

// assegnamento dei pin di collegamento e variabili

// sonar
#define echoPinFront 2 
#define trigPinFront 3 
#define echoPinRight 4 
#define trigPinRight 5 
#define echoPinLeft 6 
#define trigPinLeft 7 

// switch
#define switchFront 8
#define switchRight 9
#define switchLeft  10

void setup() {

/* ros part*/
  nh.initNode();
  nh.advertise(sensors_pub);
/* end ros part*/

  // setto la seriale
  //Serial.begin(9600);
  // setto i vari pin
  
  //sonar
  pinMode(echoPinFront, INPUT ); 
  pinMode(trigPinFront, OUTPUT ); 
  pinMode(echoPinRight, INPUT ); 
  pinMode(trigPinRight, OUTPUT ); 
  pinMode(echoPinLeft, INPUT ); 
  pinMode(trigPinLeft, OUTPUT ); 
  
  //switch
  pinMode(switchFront, INPUT);
  pinMode(switchRight, INPUT);
  pinMode(switchLeft, INPUT);

}

// funzione per il sonar
long sonarsensor(int triggerPin,int echoPin){
  long distance = 0;
  digitalWrite(triggerPin, LOW);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  long times = pulseIn(echoPin, HIGH);
  if(times<38000){
    distance = 0.034 * times /2;
    return distance; 
  }
  return distance;
}

// funzione per switch
long switchsensor(int switchpin){
  if(digitalRead(switchpin) == HIGH){
    return 1;
  }
  return 0;
}

void loop() {
/* ros part*/
  
  senso.sensori[0]=sonarsensor(trigPinFront, echoPinFront);
  senso.sensori[3]=switchsensor(switchFront);
  senso.sensori[1]=sonarsensor(trigPinRight, echoPinRight);
  senso.sensori[4]=switchsensor(switchLeft);
  senso.sensori[2]=sonarsensor(trigPinLeft, echoPinLeft);
  senso.sensori[5]=switchsensor(switchRight);

  
  sensors_pub.publish(&senso);
  nh.spinOnce();  
/* end ros part*/
  
}
