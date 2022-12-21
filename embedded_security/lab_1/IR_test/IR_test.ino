#include<IRremote.h>


int recv_pin = 6;
IRrecv receiver(recv_pin);
decode_results results;

void setup()
{
   // put your setup code here, to run once:
   Serial.begin(9600);
   receiver.enableIRIn();
}

void loop()
{
   // put your main code here, to run repeatedly:
   if (receiver.decode(&results))  // ********  added &results (a place to store the key code)
   {
      Serial.println(results.value, HEX);
      receiver.resume();
   }

}
