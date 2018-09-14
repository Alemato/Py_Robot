/* 
    Legge lo stato dei 3 sensori sonar 
*/ 

int echoPinFront = 4; 
int trigPinFront = 5; 
int echoPinRight = 8; 
int trigPinRight = 9; 
int echoPinLeft = 6; 
int trigPinLeft = 7; 
long data[3]; 
void setup () 
{ 
  pinMode (echoPinFront, INPUT ); 
  pinMode (trigPinFront, OUTPUT ); 
  pinMode (echoPinRight, INPUT ); 
  pinMode (trigPinRight, OUTPUT ); 
  pinMode (echoPinLeft, INPUT ); 
  pinMode (trigPinLeft, OUTPUT ); 
Serial.begin(9600) ; 
} 
long sonar(int triggerPin,int echoPin){ 
digitalWrite (triggerPin, LOW); 
digitalWrite (triggerPin, HIGH); 
delayMicroseconds (5); 
digitalWrite (triggerPin, LOW); 
long time = pulseIn (echoPin, HIGH); 
long distanza=0;
if(time<38000)
{
  distanza = 0.034 * time / 2; 
  return distanza; 
  }
return time; 
}

void loop (){ 
data[0] = sonar(trigPinFront,echoPinFront); 
data[1] = sonar(trigPinRight,echoPinRight); 
data[2] = sonar(trigPinLeft, echoPinLeft); 
Serial.println(String(data[0]) + "|" + String(data[1]) +"|" + String(data[2])); 
delay(100); 
}
