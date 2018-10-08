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
  long data[5];
  data[0]=sonarsensor(trigPinFront, echoPinFront);
  delay(333);
  data[3]=switchsensor(switchFront);
  data[1]=sonarsensor(trigPinRight, echoPinRight);
  delay(333);
  data[4]=switchsensor(switchLeft);
  data[2]=sonarsensor(trigPinLeft, echoPinLeft);
  delay(334);
  data[5]=switchsensor(switchRight);
  Serial.println("DATA");
  Serial.println(data[0]);
  Serial.println(data[1]);
  Serial.println(data[2]);
  Serial.println(data[3]);
  Serial.println(data[4]);
  Serial.println(data[5]);
}