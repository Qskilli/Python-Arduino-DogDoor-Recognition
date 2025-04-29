
#include <Servo.h>
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int GreenLed = 12;
int RedLed = 6;
int servoPos = 180; // Start at 90 degrees
 
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  pinMode(GreenLed, OUTPUT);
  pinMode(RedLed, OUTPUT);
}
void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim(); // Remove whitespace and newline characters
 
    if (msg == "Red") { // Human detected
      digitalWrite(RedLed, HIGH);
      digitalWrite(GreenLed, LOW);
      servoPos = 0; // Move 90° clockwise
      myservo.write(servoPos);
 
    } else if (msg == "Green") { // Dog detected
      digitalWrite(GreenLed, HIGH);
      digitalWrite(RedLed, LOW);  
      servoPos = 180; // Move 90° counterclockwise
      myservo.write(servoPos);
      
 
    } else { // No input (blank) - treat like "Red"
      digitalWrite(GreenLed, LOW);
      digitalWrite(RedLed, LOW);
      
      servoPos = 0; // Move 90° clockwise
      myservo.write(servoPos);
    }
  }
}
