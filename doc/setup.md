# Portal v3 Setup

## Hardware

The basis for the Portal is a ELV Keymatic lock that is controlled by a Raspberry Pi (in the hopes that this will prove less hacky than the previous Arduino based solution).

## Input and Output

The Raspberry Pi is connected to the local network via ethernet (which is only required if you use the timestamp feature since you need access to an ntp then) and has an Edimax wifi antennae to maintain the Portal access point. The access point is not secured since only connections via ssh will be used and there is no need to make the process more complicated.

The Raspberry Pi has an input pin (GPIO #TODO) signalling if the door is open or closed. Another input pin (GPIO #TODO) sends a signal when the buton for locking the door has been pressed. A final input pin (GPIO #TODO) signals the need for a reboot in case something has gone horribly wrong.

The output pins are optional: GPIO #TODO sends signals to sound an alarm when the door is about to lock. There will also be a display showing the current keyholder that is addressed via UART.

## Process: Opening and Closing

## Process: Managing keys
