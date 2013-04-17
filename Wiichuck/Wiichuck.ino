/*
 * Derived from WiiChuckDemo -- 2008 Tod E. Kurt, http://thingm.com/
 */

#include <Wire.h> // a library that's bundled with the Arduino IDE
#include "nunchuck_funcs.h" // this is Tod E. Kurt's library

//int ledPin = 13; // why did the demo file come with this? don't seem to need it

byte accx,accy,accz,zbut,cbut; // declaring these variables for use later
int loop_cnt=0; // counter, using it later for how frequently to collect data

void setup()
{
    Serial.begin(19200); // make sure serial monitor is set to match this for reading data
    nunchuck_setpowerpins(); // sets up analog pins 2 and 3 to be used as power and ground
    nunchuck_init(); // send the initilization handshake
    
    Serial.print("WiiChuck connected!\n");
}

void loop() // Arduino constantly runs this
{
    // starting counter variable at 0, increments by 1 every second
    // once it gets over 100, collect data and reset counter to 0
    if( loop_cnt > 100 ) { // every 100 ms get new data
        loop_cnt = 0;

        nunchuck_get_data();

        zbut = nunchuck_zbutton(); // check input from z button
        
        if ( zbut == 1 ) { // if z button is pressed down (1), collect xyz data
          accx  = nunchuck_accelx(); // ranges from approx 70 - 182
          accy  = nunchuck_accely(); // ranges from approx 65 - 173
          accz  = nunchuck_accelz();
          
          Serial.print("accx: "); Serial.print((byte)accx,DEC);
          Serial.print("\taccy: "); Serial.print((byte)accy,DEC);
          Serial.print("\taccz: "); Serial.print((byte)accz,DEC);
          Serial.print("\n");
          
        }           

    }
    loop_cnt++;
    delay(1);
}

