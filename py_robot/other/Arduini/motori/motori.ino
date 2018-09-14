/*
 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
 - Seguiamo i collegamenti come descritti nel sorgente in quanto i pin di abilitiazione dei pwm in arduino -
 * sono specifici.                                                                                         *
 - Nel dettaglio sono i pin: 11 10 9 6 5 3, o comunque quelli con una tilde disegnata.                     -
 * Per questo motivo le abilitazioni dei motori, che devono essere in PWM (a meno di motori passo passo),  *
 - devono essere collegate nei pin illustrati sopra.                                                       -
 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
 */

int ENAr = 11; //pin PWM
int IN1r = 12;
int IN2r = 13;
int IN3r = 8;
int IN4r = 9;
int ENBr = 10; //pin PWM

int ENAl = 6; //pin PWM
int IN1l = 7;
int IN2l = 2;
int IN3l = 4;
int IN4l = 3;
int ENBl = 5; //pin PWM

int speedhighM = 255;
int speedM = 200; // velocità motori (min 120 max 255, gap compreso)
int velM = 13; // fattore moltiplicativo 
int speedlowM = 150;
int rot90 = 140;

void direction(boolean dir) {
  if (dir) {
    digitalWrite(IN1r, 0);
    digitalWrite(IN2r, 1);
    digitalWrite(IN3r, 0);
    digitalWrite(IN4r, 1);  
    digitalWrite(IN1l, 0);
    digitalWrite(IN2l, 1);
    digitalWrite(IN3l, 0);
    digitalWrite(IN4l, 1);      
  } else {
    digitalWrite(IN1r, 1);
    digitalWrite(IN2r, 0);
    digitalWrite(IN3r, 1);
    digitalWrite(IN4r, 0);  
    digitalWrite(IN1l, 1);
    digitalWrite(IN2l, 0);
    digitalWrite(IN3l, 1);
    digitalWrite(IN4l, 0);    
  }
}

void motors(int a, int b, int c, int d) {
    analogWrite(ENAr, a); // Attiva il motore A destro
    analogWrite(ENBr, b); // Attiva il motore B destro   
    analogWrite(ENAl, c); // Attiva il motore A sinistro
    analogWrite(ENBl, d); // Attiva il motore B sinistro
}

void forward (int value) { 
  halt();
  if (value>=0 && value<10) {
    direction(true); // forward
    speedM = 138+velM*value;
    motors(speedM, speedM, speedM, speedM);
  }
}

void forward1left (void) { 
  halt();
  direction(true);
  motors(speedhighM, speedhighM, 0, speedhighM);
}

void forward1right (void) {
  halt();
  direction(true);
  motors(speedhighM, 0, speedhighM, speedhighM);
}

void left90 (void) {
  halt();
  digitalWrite(IN1r, 0);
  digitalWrite(IN2r, 1);
  digitalWrite(IN3r, 0);
  digitalWrite(IN4r, 1);  
  digitalWrite(IN1l, 1);
  digitalWrite(IN2l, 0);
  digitalWrite(IN3l, 1);
  digitalWrite(IN4l, 0);
  analogWrite(ENAr, speedhighM); 
  analogWrite(ENBr, 0);   
  analogWrite(ENAl, speedhighM); 
  analogWrite(ENBl, speedhighM); 
  delay (rot90);
  halt();
}

void right90 (void) { 
  halt();
  digitalWrite(IN1r, 1);
  digitalWrite(IN2r, 0);
  digitalWrite(IN3r, 1);
  digitalWrite(IN4r, 0);
  digitalWrite(IN1l, 0);
  digitalWrite(IN2l, 1);
  digitalWrite(IN3l, 0);
  digitalWrite(IN4l, 1);
  analogWrite(ENAr, speedhighM); 
  analogWrite(ENBr, speedhighM);    
  analogWrite(ENAl, 0); 
  analogWrite(ENBl, speedhighM); 
  delay (rot90);
  halt();
}

void backSlow(void){
  halt();
  direction(false);
  motors(speedlowM, speedlowM, speedlowM, speedlowM);
}
 

void halt(void) { 
  digitalWrite(IN1r, 0);
  digitalWrite(IN2r, 0);
  digitalWrite(IN3r, 0);
  digitalWrite(IN4r, 0);
  digitalWrite(IN1l, 0);
  digitalWrite(IN2l, 0);
  digitalWrite(IN3l, 0);
  digitalWrite(IN4l, 0);
  motors(0,0,0,0);
} 

void setup(){
  pinMode(ENAr, OUTPUT);
  pinMode(ENBr, OUTPUT);
  pinMode(IN1r, OUTPUT);
  pinMode(IN2r, OUTPUT);
  pinMode(IN3r, OUTPUT);
  pinMode(IN4r, OUTPUT);
  
  pinMode(ENAl, OUTPUT);
  pinMode(ENBl, OUTPUT);
  
  pinMode(IN1l, OUTPUT);
  pinMode(IN2l, OUTPUT);
  pinMode(IN3l, OUTPUT);
  pinMode(IN4l, OUTPUT);
  
  analogWrite(ENAr,0); // blocca il motore A destro
  analogWrite(ENBr,0); // blocca il motore B destro
  
  analogWrite(ENAl,0); // blocca il motore A sinistro
  analogWrite(ENBl,0); // blocca il motore B sinistro

  Serial.begin(9600); // setto la speedM della trasmissione seriale 
  delay (3000);
  Serial.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
  Serial.println("4 wheels drive rover by IRSLab @ UnivAQ");
  Serial.println("commands:");
  Serial.println("a b c d e f g h i j: forward speed levels");
  Serial.println("l r: turn left or right");
  Serial.println("w z: forward with a long turn left(w) or right(z)");
  Serial.println(". : slow back");
  Serial.println("space : HALT");
} 

char cmd;
char value;

void loop(){
  if (Serial.available() > 0) {
      cmd = Serial.read(); //leggo dalla seriale
      char choise = cmd;
      switch(choise){
        case 'a': forward(0);  break;
        case 'b': forward(1);  break;
        case 'c': forward(2);  break;  
        case 'd': forward(3);  break;  
        case 'e': forward(4);  break;  
        case 'f': forward(5);  break;   
        case 'g': forward(6);  break;
        case 'h': forward(7);  break;      
        case 'i': forward(8);  break;
        case 'j': forward(9);  break;      
        case 'l': left90();  break;
        case 'r': right90();  break;
        case 'w': forward1left();  break;
        case 'z': forward1right();  break;
        case '.': backSlow();  break;
        case ' ': halt();  break;
    }
  }
}
