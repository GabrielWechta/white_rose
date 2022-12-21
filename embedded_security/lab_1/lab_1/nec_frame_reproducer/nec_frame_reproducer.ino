#include <IRremote.h>

IRsend irsend;
unsigned int buf[3];
unsigned long sample1_hex = 0x4CB3817E;
unsigned long sample2_hex = 0x4CB3619E;

void setup() {
    Serial.begin(9600);
    buf[0] = 9000;  // Mark 9ms
    buf[1] = 2250;  // Space 2.25ms
    buf[2] = 560;   // Burst
}

void replay_sample(unsigned long sample_hex){
    irsend.sendNEC(sample_hex, 32);
    delay(40);
    irsend.sendRaw(buf, 3, 38);
    delay(96);
    irsend.sendRaw(buf, 3, 38);
}

void loop() {
    delay(1000);
    replay_sample(sample1_hex);
    Serial.println("I sent sample 1.");

    delay(1000);
    replay_sample(sample2_hex);
    Serial.println("I sent sample 2.");
}