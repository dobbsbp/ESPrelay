# ESPrelay
Sender and reciever for remotely opening and closing a circuit.

# Two parts

## Wifi Relay

Located in the wifirelay/src folder is located the code for an esp8266 (in my case Wemos d1 mini).  This code creates a webserver that allows for connections that put gpio 07 to either high or low state.  With my electronics, I have this set up to control a relay for AC power.

## Wifi Switch

Located in the wifiswitch/src folder is the code for creating a wireless switch for the relay.  What this code does is connect to the wifi relay and simply access a specific address on the webserver via the client.connect( ) command.

# Known Issues
I had this connected to my router at home and it seemed to have a delay of maybe 1 second or so.  I was expecting something a bit more instantaneous but i'm okay with the delay.  I have yet to test this directly from esp to esp device.  will do this in the near future.

# Micropython
Now working on a micropython implementation for wemos.  Micropython is great for programming these little devices.  I struggle so much with arduino/C/C++/basically anything and have found python to be a bit easier to work with.
