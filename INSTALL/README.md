# Install MarCANex

The MarCANex framework comes with build scripts for its three major functions:

- Command and Control Beacon (a device connected to a NMEA 2000 network like a raspberry pi)
- Command and Control Server (tested on debian-based distros)
    - Console (CLI only)
    - Web Server and Console

## Beacon Install Script

```
curl -s https://raw.githubusercontent.com/Jstith/MarCANex/main/INSTALL/build_beacon.sh -o build_beacon.sh && chmod +x build_beacon.sh && ./build_beacon.sh
```