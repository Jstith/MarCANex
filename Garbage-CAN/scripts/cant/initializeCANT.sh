#!/bin/bash

screen -S CANT -dm /dev/ttyACM0 115200 #initalize the cant
screen -S CANT -p 0 -X stuff "^M"
screen -S CANT -p 0 -X stuff "3"
screen -S CANT -p 0 -X stuff "^M"
screen -S CANT -p 0 -X stuff "500000"
screen -S CANT -p 0 -X stuff "^M"