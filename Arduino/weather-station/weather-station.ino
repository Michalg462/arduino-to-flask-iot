#include <LiquidCrystal.h>
#include "DHT.h"

// LCD object creation
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// humidity sensor declaration
DHT dht;

// Custom characters
byte celcius[8] ={
  0b01000,
  0b10100,
  0b01000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

byte thermometer[8] ={
  B01100,
  B01100,
  B01100,
  B01100,
  B01100,
  B11110,
  B11110,
  B01100
};

byte humidity[8] = {
  B00100,
  B00100,
  B01110,
  B01110,
  B11111,
  B11111,
  B11111,
  B01110
};


void setup() {
  // LCD initialization
  lcd.begin(16, 2);
  lcd.clear();

  // loading custom chars
  lcd.createChar(0, celcius);
  lcd.createChar(1, thermometer);
  lcd.createChar(2, humidity);

  // Pin modes
  pinMode(A5, INPUT);

  // DHT setup
  dht.setup(2);

  // Serial monitor for debug 
  Serial.begin(9600);

  // setup complete
  lcd.setCursor(0,0);
  lcd.print("Ready to go!");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Checks if there is something to read on a Serial
  if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');

        // When 'GET' command is sent, 
        // read the data from sensors and send it back via Serial 
        if (cmd == "GET"){
            int humi = dht.getHumidity();

            float volt = analogRead(A5);
            float temp = volt/1023*5 * 100;

            // Additionally prints the measured values on LCD screen
            lcd.setCursor(0, 0);
            lcd.write(1);
            lcd.print(temp);
            lcd.write(byte(0));
            lcd.print("C");

            lcd.setCursor(0, 1);
            lcd.write(2);
            lcd.print(humi);
            lcd.print("%");

            Serial.print(temp);
            Serial.print(";");
            Serial.println(humi);
        }

  }

  // The DHT11 allows for measurements every 1 second, for safety let's delay this for two
  delay(2);
}
