// Define pins
#define MoistureRead A0
#define MoisturePWR 3

// Initiate values
int moisture;

void setup(){
  Serial.begin(9600);
  }

int get_moisture() {
  // Sensor is turned off between reading due to corrosion.
  digitalWrite(MoisturePWR, HIGH);    // Sensor on
  delay(10);
  int value = analogRead(MoistureRead);   // Get reading
  digitalWrite(MoisturePWR, LOW);     // Sensor off
  return value;
  }

void loop() {
  moisture = get_moisture();
  Serial.print("Moisture: ");
  Serial.println(moisture);

  delay(100);
  }
