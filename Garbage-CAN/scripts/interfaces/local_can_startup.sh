#!/bin/bash

if [ -z "$1" ]
    then
        echo "Run with bitrate as argument"
    else
	ifconfig can0 down
        ip link set can0 type can bitrate "$1"
        ifconfig can0 txqueuelen 10000
        ifconfig can0 up
fi
