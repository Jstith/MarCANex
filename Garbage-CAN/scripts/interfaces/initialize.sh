#!/bin/bash

echo "250k Baud on can0"
ip link set can0 type can bitrate 250000
ifconfig can0 up

# Optional - trying to make sure we get all data in a FD-CAN message
ifconfig can0 txqueuelen 1024
