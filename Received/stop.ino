const int stopPin = 13;  // LED or motor pin for stop
     const int movePin = 12;  // LED or motor pin for move

     void setup() {
       pinMode(stopPin, OUTPUT);
       pinMode(movePin, OUTPUT);
       Serial.begin(9600);  // Match baud rate with Python script
       digitalWrite(stopPin, LOW);
       digitalWrite(movePin, LOW);
     }

     void loop() {
       if (Serial.available() > 0) {
         char signal = Serial.read();
         if (signal == '1') {
           digitalWrite(stopPin, HIGH);  // Stop the robot
           digitalWrite(movePin, LOW);
           delay(3000);  // Hold for 3 seconds (matching Python sleep)
           digitalWrite(stopPin, LOW);   // Resume after 3 seconds
         } else if (signal == '0') {
           digitalWrite(stopPin, LOW);   // Keep moving
           digitalWrite(movePin, HIGH);
         }
       }
     }