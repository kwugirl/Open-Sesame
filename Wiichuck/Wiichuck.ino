/*
 * Derived from WiiChuckDemo -- 2008 Tod E. Kurt, http://thingm.com/
 */

#include <Wire.h> // a library that's bundled with the Arduino IDE
#include "nunchuck_funcs.h" // this is Tod E. Kurt's library
#include "Timer.h" // Timer library http://playground.arduino.cc//Code/Timer

byte accx,accy,accz,zbut; // declaring these variables for use later
int status = 0; // track whether status on (1) or off (0)
Timer t;

void setup()
{
    Serial.begin(19200); // make sure serial monitor is set to match this for reading data
    nunchuck_setpowerpins(); // sets up analog pins 2 and 3 to be used as power and ground
    nunchuck_init(); // send the initilization handshake
    
    t.every(1, takeReading);
    
    Serial.print("WiiChuck connected!\n");
}

void loop() // Arduino constantly runs this
{
  t.update();
}

void takeReading() 
{
    nunchuck_get_data();

    zbut = nunchuck_zbutton(); // check input from z button
    
    if ( zbut == 1 ) { // if z button is pressed down (1)
      if ( status == 0 ) { // if Arduino weren't previously collecting info
        status = 1;
        Serial.println("start");
      }          
      
      accx  = nunchuck_accelx(); // ranges from approx 70 - 182
      accy  = nunchuck_accely(); // ranges from approx 65 - 173
      accz  = nunchuck_accelz();
      
      Serial.print((byte)accx,DEC); Serial.print(","); // x reading
      Serial.print((byte)accy,DEC); Serial.print(","); // y reading
      Serial.println((byte)accz,DEC); // z reading
      
    }
    else {
      if( status == 1) { // if Arduino were previously collecting data
        Serial.println("stop");
        status = 0;
      }
    }
}

