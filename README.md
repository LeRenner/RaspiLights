# RaspiLights
A simple python script for controlling lights with a Raspberry Pi.

This script controls the state of two lamps, that are connected to GPIO pins 2 and 4, based on the state of three buttons, that are connected to GPIO pins 17, 22 and 27. It also allows the lamps to be controlled from a remote computer thought SSH.

This script is made to work with three buttons: one for each light, and one that controls both. One important thing to consider is that this program deals with changes in the state of the buttons, not the absolute state, so their usage may be inverted over time.

## Installation

### Hardware
For each button, wire one contact to ground, and the other to its GPIO pin. Note that you can use the same ground pin for all the buttons, as ground GPIOs are not very numerous on a Raspberry Pi.

The most simple way to control a lamp is using a relay. Most relay modules use vcc and ground pins to power it up, as well as one or more wires that control the actuation of the relay. In that case, you should wire vcc and ground, as well as pins 2 and 4 to the pins on the module.

Note: Aways remember to be very careful while working with main power. If you don't know what you are doing, you should ask someone else's help with that part.


### Software
As this programs interacts with other files, its directory has to be on a specific location of your computer to work without having to be edited. Because of that, you should either use the user Pi, or edit the locations on the script to reflect the actual locations on your computer.

First, clone a copy of the repository on your Raspberry Pi. You can do that typing the following command on your terminal, while you are on your home folder:

    git clone https://github.com/LeRenner/RaspiLights/

After that, you should test the program. For this, enter the directory that contains the program, and then run it to see if everything is working properly:

    cd RaspiLights
    python3 lights.py

After that, you can stop the script with Ctrl+C, and make that script start at boot, so you don't have to run it everytime the Raspberry pi is restarted. To make that happen, edit `/etc/rc.local` and add one line, right before `exit 0`:

    sudo python3 /home/pi/RaspiLights/lights.py &

After doing that, you can restart your Raspberry Pi, to see if the program is being run at boot as expected.

## Usage
As previously mentioned, you can control the state of the lights using a remote computer or smartphone with SSH. The way you interact with the script is very simple. You just have to create an empty file at /home/pi/RaspiLights with the command touch. The name of the file determines what it does to the state of the lights:

```
switch1 -> switch lamp 1
switch2 -> switch lamp 2
switch  -> switch both lamps
off     -> turn lamps off (regardless of their state)
```
If you want to switch lamp 1, for example, all you have to do is SSH into the Raspberry Pi and type:

    touch /home/pi/RaspiLights/switch1

The script will detect the file, switch the lamps, an then remove it.
