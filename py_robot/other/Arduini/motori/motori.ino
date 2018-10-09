#include <L298N.h>

#include <ros.h>
#include <ArduinoHardware.h>
#include <py_robot/Motor_Switch_Node.h>
#include <py_robot/Controller_Node.h>

ros::NodeHandle nh;


char cmd;
int vel;


void CallBack( const py_robot::Controller_Node& velo){
    cmd = velo.velo;
}


ros::Subscriber<py_robot::Controller_Node> motor_sub("velo", CallBack);

py_robot::Motor_Switch_Node switches;
ros::Publisher switch_pub("switches", &switches);


// motori 1 e 2

#define AIN1 2
#define AIN2 4
#define PWMA 3

// motori 3 e 4
#define BIN1 5
#define BIN2 7
#define PWMB 6


// switch
#define switchFront 8
#define switchLeft 9
#define switchRight 10



L298N sinistra(PWMA, AIN1, AIN2, AIN1, AIN2, PWMA);
L298N destra(PWMB, BIN1, BIN2, BIN1, BIN2, PWMB);

int time_delay = 2;


void setup() {

  nh.initNode();
  nh.advertise(switch_pub);
  nh.subscribe(motor_sub);

  //switch
  pinMode(switchFront, INPUT);
  pinMode(switchRight, INPUT);
  pinMode(switchLeft, INPUT);


}


// funzione per switch
long switchsensor(int switchpin){
  if(digitalRead(switchpin) == HIGH){
    delay(30);
    if(digitalRead(switchpin) == HIGH){
    return 0;
  }}
  return 1;
}


void VaiAvanti(int vel) {
  sinistra.forward(vel, time_delay);
  destra.forward(vel, time_delay);
  
  }

void VaiIndietro(int vel) {
  sinistra.backward(vel, time_delay);
  destra.backward(vel, time_delay);
  
  }
void VaiSinistra() {
  sinistra.backward(100, 2000);
  destra.forward(100, 2000);
  }

void VaiDestra() {
  sinistra.forward(100, 2000);
  destra.backward(100, 2000);
  }


void loop() {

  
      switch(cmd){
        
        case 'a': VaiAvanti(70);
          break;      

        case 'b': VaiAvanti(90);
          break;           

        case 'c': VaiAvanti(110);
          break;    

         case 'd': VaiAvanti(130);
          break;      

        case 'e': VaiAvanti(150);
          break;  

        case 'f': VaiAvanti(170);
          break;

        case 'g': VaiAvanti(190);
          break;    

         case 'h': VaiAvanti(210);
          break;      

        case 'i': VaiIndietro(80);
          break;  

        case 'l': VaiIndietro(100);
          break;
        
        case 'm': VaiIndietro(150);
          break;
       
        case 'o': VaiIndietro(180);
          break;
        
        case 'p': VaiIndietro(210);
          break;
        
        case 'q': VaiSinistra();
          break;
        
        case 'r': VaiDestra();
          break;     
      }

    //switch part
    switches.switches[0]=switchsensor(switchFront);
    switches.switches[1]=switchsensor(switchLeft);
    switches.switches[2]=switchsensor(switchRight);

    switch_pub.publish(&switches);
    nh.spinOnce(); 
    delay(10);
    }
 
