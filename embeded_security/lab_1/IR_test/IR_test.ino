#include <IRremote.hpp>
const int IR_RECEIVE_PIN = 7;

void setup()
{
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
}

void loop() {
  if (IrReceiver.decode()) {
      Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
      // IrReceiver.printIRResultShort(&Serial); // optional use new print version
      
      IrReceiver.resume(); // Enable receiving of the next value
  }
  
}