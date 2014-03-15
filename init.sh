#!/bin/sh
#RasPi GPIO setup

# 4 outputs, 3 inputs

#keymatic open
gpio mode 0 output

#keymatic close
gpio mode 1 output

#button LED
gpio mode 2 output

#buzzer
gpio mode 3 output

#init outputs to 5 to 5V
gpio write 0 1
gpio write 1 1
gpio write 2 1
gpio write 3 1

#button
gpio mode 4 input

#doorswitch
gpio mode 5 input

#lockswitch
gpio mode 6 input
