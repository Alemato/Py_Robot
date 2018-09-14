String cmd;

String whois(String cmd) {
    if (cmd == "whois"){
      Serial.println("Nome");
    }else {
      return cmd;
    }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    cmd = Serial.readString();
    if (whois(cmd) == cmd){
      Serial.println("comando");
    }
  }
}
