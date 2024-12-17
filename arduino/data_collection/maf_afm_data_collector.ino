const int mafPin = A0; // MAF sensor connected to analog pin A0
const int afmPin = A1; // AFM sensor connected to analog pin A1

void setup() {
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Read voltage from MAF sensor
  int mafValue = analogRead(mafPin);
  float mafVoltage = mafValue * (5.0 / 1023.0); // Convert the value to voltage

  // Read voltage from AFM sensor
  int afmValue = analogRead(afmPin);
  float afmVoltage = afmValue * (5.0 / 1023.0); // Convert the value to voltage

  // Send the data over serial
  Serial.print(mafVoltage);
  Serial.print(",");
  Serial.print(afmVoltage);
  Serial.println();
}
