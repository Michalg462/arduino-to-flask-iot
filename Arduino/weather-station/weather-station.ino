#include <LiquidCrystal.h>
#include <TimerOne.h>
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

byte drop[8] = {
  B00100,
  B00100,
  B01110,
  B01110,
  B11111,
  B11111,
  B11111,
  B01110
};

// global variables

float temperature = 0;
int humidity = 0;


void setup() {
  // LCD initialization
  lcd.begin(16, 2);
  lcd.clear();

  // loading custom chars
  lcd.createChar(0, celcius);
  lcd.createChar(1, thermometer);
  lcd.createChar(2, drop);

  // Pin modes
  pinMode(A5, INPUT);

  // DHT setup
  dht.setup(2);

  // Starting a timer for communication via Serial
  Timer1.initialize(1000000);
  Timer1.attachInterrupt(listen);

  // Serial monitor for debug 
  Serial.begin(9600);

  // waitng for the DHT11 to make a first reading 

  delay(1100);
}

void loop() {
  // measure the values of temperature and humidity
  humidity = dht.getHumidity();

  // delay for communication
  delay(1100);

  float volt = analogRead(A5);
  temperature = volt/1023*5 * 100;

  // Print the measured values on LCD screen
  lcd.setCursor(0, 0);
  lcd.write(1);
  lcd.print(temperature);
  lcd.write(byte(0));
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.write(2);
  lcd.print(humidity);
  lcd.print("%");
  // The DHT11 allows for measurements every 1 second, but for now it will be enough to measure around every 5 seconds 
  // (4 delay and 1 waiting for humidity sensor readings)
  delay(4000);
}

void listen(){
   // Checks if there is something to read on a Serial
  if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');

        // When 'GET' command is sent, 
        // send the current data to server
        if (cmd == "GET"){
            Serial.print(temperature);
            Serial.print(";");
            Serial.println(humidity);
        }
  }
}
