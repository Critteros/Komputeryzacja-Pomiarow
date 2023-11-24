#define SENSE_PIN  A0  // Change this to the pin connected to your LED

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(50);
}

float readCelsius()
{ 
  float ADCres = 1023.0;
  int Beta = 3950;      // Beta parameter
  float Kelvin = 273.15; // 0°C = 273.15 K
  int Rb = 10000;      // 10 kOhm
  float Ginf = 120.6685; // Ginf = 1/Rinf
  float Rthermistor = Rb * (ADCres / analogRead(SENSE_PIN) - 1);
  float _temperatureC = Beta / (log( Rthermistor * Ginf )) ;

  return _temperatureC - Kelvin;
}

void loop()
{
  Serial.println(readCelsius());
  delay(1000);
}