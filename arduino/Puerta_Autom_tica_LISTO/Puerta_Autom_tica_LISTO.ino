#include <SPI.h>
#include <MFRC522.h>#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

//Crear el objeto lcd  dirección  0x3F y 16 columnas x 2 filas
LiquidCrystal_I2C lcd(0x27,16,2);  //
 
#define SS_PIN 10
#define RST_PIN 9
#define LED_G 5 //define green LED pin
#define LED_R 4 //define red LED
#define RELAY 3 //relay pin
#define BUZZER 2 //buzzer pin
#define ACCESS DELAY 1000
#define DENIED_DELAY 1000
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

enum State {
  LOCKED,
  UNLOCKED
};

State currentState = LOCKED;
 
void setup() 
{
     // Inicializar el LCD
  lcd.init();
  
  //Encender la luz de fondo.
  lcd.backlight();
  
  // Escribimos el Mensaje en el LCD.
  lcd.setCursor(3,0);
  lcd.print("Bienvenido");
  
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();          // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  pinMode(LED_G, OUTPUT); // los led son salidas
  pinMode(LED_R, OUTPUT);
  pinMode(RELAY, OUTPUT); // salida del relay
  pinMode(BUZZER, OUTPUT); // salida del buzzer, que es la bocina
  noTone(BUZZER); // tono del buzzer
  digitalWrite(RELAY, LOW); //el relay va a comenzar apagado
  Serial.println("Put your card to the reader..."); //mensaje que va a salir en la pantalla
  Serial.println();

}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :"); // muestra el UID de la tarjeta en el monitor
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "); //muestra en el monitor serie el UID de cada tarjeta
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ")); // conjunto de los carácteres del UID
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");//es el mensaje de Access denied o Authorized access dependiendo de que tarjeta acerquemos


  content.toUpperCase(); // PREGUNTAR AL PROFE
  if (content.substring(1) == "A3 C1 E5 16") //change here the UID of the card/cards that you want to give access
  { 
    if (currentState == LOCKED){
      lcd.clear();
    lcd.print("Abierto");
    delay(500);
    Serial.println("Authorized access");
    Serial.println();
     digitalWrite(LED_R, LOW);
     tone(BUZZER, 300);
    delay(500); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, HIGH);
    digitalWrite(LED_G, HIGH);
    noTone(BUZZER); // tono del buzzer
     currentState = UNLOCKED;
  }
  else {
            lcd.clear();
    lcd.print("Cerrado");
    Serial.println("Authorized access");
    Serial.println();
    digitalWrite(LED_R, HIGH);
     tone(BUZZER, 300);
    delay(1000); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, LOW);
    digitalWrite(LED_G, LOW);
    noTone(BUZZER); // tono del buzzer
     currentState = LOCKED;
  }
  }
  else if (content.substring(1) == "13 86 2C 11") //change here the UID of the card/cards that you want to give access
  {
 if (currentState == LOCKED){
  lcd.clear();
    lcd.print("Abierto");
    delay(500);
    Serial.println("Authorized access");
    Serial.println();
     digitalWrite(LED_R, LOW);
     tone(BUZZER, 300);
    delay(500); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, HIGH);
    digitalWrite(LED_G, HIGH);
    noTone(BUZZER); // tono del buzzer
     currentState = UNLOCKED;
  }
  else {
            lcd.clear();
    lcd.print("Cerrado");
    Serial.println("Authorized access");
    Serial.println();
    digitalWrite(LED_R, HIGH);
     tone(BUZZER, 300);
    delay(1000); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, LOW);
    digitalWrite(LED_G, LOW);
    noTone(BUZZER); // tono del buzzer
     currentState = LOCKED;
  }

  }
  else if (content.substring(1) == "D3 DA 44 97") //change here the UID of the card/cards that you want to give access
  {
    if (currentState == LOCKED){
    lcd.clear();
    lcd.print("Abierto");
    delay(500);
    Serial.println("Authorized access");
    Serial.println();
     digitalWrite(LED_R, LOW);
     tone(BUZZER, 300);
    delay(500); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, HIGH);
    digitalWrite(LED_G, HIGH);
    noTone(BUZZER); // tono del buzzer
     currentState = UNLOCKED;
  }
  else {
        lcd.clear();
    lcd.print("Cerrado");
    Serial.println("Authorized access");
    Serial.println();
    digitalWrite(LED_R, HIGH);
     tone(BUZZER, 300);
    delay(1000); // si la tarjeta 1 está autorizada va a salir el mensaje durante 0.5 segundos
    digitalWrite(RELAY, LOW);
    digitalWrite(LED_G, LOW);
    noTone(BUZZER); // tono del buzzer
     currentState = LOCKED;
  }
 
  }
 
 
 else   {
      lcd.clear();
    lcd.print("Acceso denegado");
    Serial.println(" Access denied"); // si la tarjeta no está autorizada, aparece este mensaje en la pantalla
    digitalWrite(LED_R, HIGH); // el led rojo se prende
    tone(BUZZER, 300);
    delay(DENIED_DELAY); // tiempo que dura el mensaje
    digitalWrite(LED_R, LOW); // pasado el tiempo se apaga el led rojo
    noTone(BUZZER); // tono del buzzer
  }

  
}
