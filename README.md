# MarCANex - NMEA 2000 Command and Control

![](.resources/../.resources/marcanex_logo.png)

The **Maritime CAN Bus Exploitation** Framework (MarCANex) is a lightweight command and control entity designed for hacking NMEA 2000 networks on maritime platforms. The MarCANex project includes attack execution software, a custom command and control implementation, and a web interface to launch and monitor attacks from.

## Organization

### [Garbage-CAN User Interface Software](Garbage-CAN/ReadMe.md)

- Originally designed for car hacking and refactored for C2, the Garbage-CAN is the web-based user interface used to manage nodes, launch attacks, and exfiltrate data.
- The Garbage-CAN server runs on python flask and SQLite.

### [C-2PO Command and Control / Exploitation Software](C-2PO/readme.md)

- Command and Control for Protocols Offshore (C-2PO) is the custom command and control software for the MarCANex framework.
- C-2PO includes beaconing functionality, diverse networking options, and end-to-end encryption.
- C-2PO client and server code utilizes multithreading to support multiple attacks at once.