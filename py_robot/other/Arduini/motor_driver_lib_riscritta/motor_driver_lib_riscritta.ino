// assegnamento pin motori 1 e 2
#define SXIN1 2
#define SXIN2 4
#define SXPWM 3

// assegnamento pin motori 3 e 4
#define DXIN1 5
#define DXIN2 7
#define DXPWM 6

char cmd;

void vaiAvanti(int vel, int tempo) {
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1, 1);
  digitalWrite(DXIN2, 0);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
}

void vaiIndietro(int vel, int tempo) {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);

  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 1);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo();
}

void vaiSinistra(int vel, int tempo) {
  digitalWrite(SXIN1, 1);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 1);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo();
}

void vaiDestra(int vel, int tempo) {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 1);

  digitalWrite(DXIN1, 1);
  digitalWrite(DXIN2, 0);

  analogWrite(SXPWM, vel);
  analogWrite(DXPWM, vel);

  delay(tempo);
  fermo();
}

void fermo() {
  digitalWrite(SXIN1, 0);
  digitalWrite(SXIN2, 0);

  digitalWrite(DXIN1, 0);
  digitalWrite(DXIN2, 0);

  analogWrite(SXPWM, 0);
  analogWrite(DXPWM, 0);
}


void setup() {
  Serial.begin(9600);
  Serial.println("Scrivi un comando");

  pinMode(SXPWM, OUTPUT);
  pinMode(SXIN1, OUTPUT);
  pinMode(SXIN2, OUTPUT);

  pinMode(DXPWM, OUTPUT);
  pinMode(DXIN1, OUTPUT);
  pinMode(DXIN2, OUTPUT);

  analogWrite(SXPWM, 0);
  analogWrite(DXPWM, 0);

  delay(1000);
}

void loop() {
  cmd = Serial.read();
  switch (cmd) {

    case 'a': vaiAvanti(70, 2000);
      break;

    case 'b': vaiAvanti(90, 2000);
      break;

    case 'c': vaiAvanti(110, 2000);
      break;

    case 'd': vaiAvanti(130, 2000);
      break;

    case 'e': vaiAvanti(150, 2000);
      break;

    case 'f': vaiAvanti(170, 2000);
      break;

    case 'g': vaiAvanti(190, 2000);
      break;

    case 'h': vaiAvanti(210, 2000);
      break;

    case 'i': vaiIndietro(80, 2000);
      break;

    case 'l': vaiIndietro(100, 2000);
      break;

    case 'm': vaiIndietro(150, 2000);
      break;

    case 'o': vaiIndietro(180, 2000);
      break;

    case 'p': vaiIndietro(210, 2000);
      break;

    case 'q': vaiSinistra(100, 2000);
      break;

    case 'r': vaiDestra(100, 2000);
      break;

    case 's': fermo();
      break;

    case 't': vaiSinistra(100, 500);        // correzione a sinistra
      break;

    case 'u': vaiDestra(100, 500);          // correzione a destra
      break;
  }
  delay(2000);
}
