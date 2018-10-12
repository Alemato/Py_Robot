
#include <ros.h>
#include <py_robot/Sonar_Volt_Node.h>

ros::NodeHandle nh;


// assegnamento dei pin di collegamento e variabili

// sonar
#define echoPinFront 2
#define trigPinFront 3
#define echoPinRight 4
#define trigPinRight 5
#define echoPinLeft 6
#define trigPinLeft 7

py_robot::Sonar_Volt_Node sonar_volt_msg;
ros::Publisher sonar_volt_pub("sonar_volt_sub", &sonar_volt_msg);




// voltmeter
int analogInput = 0;
float vout = 0.0;
float vin = 0.0;
float R1 = 100000.0; // resistance of R1 (100K) -see text!
float R2 = 10000.0; // resistance of R2 (10K) - see text!
int value = 0;


void setup() {
  nh.initNode();
  nh.advertise(sonar_volt_pub);
  pinMode(analogInput, INPUT);
  // setto la seriale
  Serial.begin(9600);
  // setto i vari pin

  //sonar
  pinMode(echoPinFront, INPUT );
  pinMode(trigPinFront, OUTPUT );
  pinMode(echoPinRight, INPUT );
  pinMode(trigPinRight, OUTPUT );
  pinMode(echoPinLeft, INPUT );
  pinMode(trigPinLeft, OUTPUT );


}

// funzione per il sonar
long sonarsensor(int triggerPin, int echoPin) {
  long distance = 0;
  digitalWrite(triggerPin, LOW);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  long times = pulseIn(echoPin, HIGH);
  if (times < 38000) {
    distance = 0.034 * times / 2;
    return distance;
  }
  return distance;
}


void loop() {
  sonar_volt_msg.sonar[0] = sonarsensor(trigPinFront, echoPinFront);
  delay(333);
  sonar_volt_msg.sonar[1] = sonarsensor(trigPinRight, echoPinRight);
  delay(333);
  sonar_volt_msg.sonar[2] = sonarsensor(trigPinLeft, echoPinLeft);
  delay(334);
  
  value = analogRead(analogInput);
  vout = (value * 5.0) / 1024.0; // see text
  vin = vout / (R2 / (R1 + R2));
  if (vin < 0.09) {
    vin = 0.0; //statement to quash undesired reading !
  }
  sonar_volt_msg.volt = vin;
  
  sonar_volt_pub.publish(&sonar_volt_msg);
  nh.spinOnce();
  delay(100);
}
