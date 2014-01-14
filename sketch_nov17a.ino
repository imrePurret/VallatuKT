//int sensor1 = analogRead(A0);
//int sensor2 = analogRead(A1);
//int sensor3 = analogRead(A2);
//int sensor4 = analogRead(A3);
//int must = 165; //kalibreerida vaja //kalibreerida vaja
//int milline;
int sensorIR = analogRead(A0);
int tyhjus = 800; //kalibreerida vaja
const int air = 7;
const int tribb = 10;
int bangbang;

void setup() {
  Serial.begin(9600);
  pinMode(air, OUTPUT);
  pinMode(tribb, OUTPUT);
  digitalWrite(tribb, HIGH);
}

void loop() {
  //sensor1 = analogRead(A0);
  //sensor2 = analogRead(A1);
  //sensor3 = analogRead(A2);
  //sensor4 = analogRead(A3);
  sensorIR = analogRead(A0);
 
if (sensorIR>tyhjus) {
  Serial.println(69);
} 
else {
  Serial.println(96); 
}

bangbang = Serial.read();

if (bangbang == 49) {
  digitalWrite(tribb, LOW);
  delay(100);
  digitalWrite(air, HIGH);
  delay(200); //Kalibreerida vaja
  digitalWrite(air, LOW);
  digitalWrite(tribb, HIGH);
}

}

