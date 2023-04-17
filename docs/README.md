---
description: The starting point
---

# Replay Attacks

## What is a Replay Attack?

A replay attack broadly refers to a malicious action that involves recording legitimate information going form one place to another, then transmitting that information again at a later time, pretending to be the original source sending it. For example, if a victim sends a username and password to a server, an attacker could record that message, save it, and replay it later to log in on the same server.&#x20;

Despite their simplicity, replay attacks can be quite powerful. If a tool or service is not properly configured to make multiple requests of the same variety somehow different from each other, replay attacks can bypass all sorts of authentication and encryption. Replay attacks are used everywhere from bypassing encrypted authentication to unlocking cars without a key fob.

## Replay attacks on NMEA 2000

There are a couple of features on NMEA 2000 networks that make replay attacks particularly effective.

### Lack of Encryption

There is no data encryption on a NMEA 2000 network. That means all data going through the wire can be read and interpreted by any device connected to it (including ours). While a replay attack could be used to send encrypted data as well, the lack of encryption makes it easier for attackers to see and understand what messages they are receiving and sending on the network.

### Lack of Authentication

There is no authentication natively included on a NMEA 2000 network. This means that devices receiving data perform no checks or challenges to see where the data is coming from. The only information provided in the data string is an 8 bit source address. But, any device is free to transmit at any source address, and in many cases the source address makes no difference to the device receiving data.

### Broadcast Protocol

NMEA 2000 networks sit on the CAN-BUS protocol, which is a broadcast-based protocol. This means that messages on the network are sent to every device on the network, rather than to a specific recipient. This feature, while great for ensuring data is delivered with a high degree of accuracy, make it quite easy for attackers to carry out replay attacks. There is no need to worry about what route the data is taking to reach its destination and if those routes have changed since the data was recorded, because every message reaches every device on a CAN-BUS network.

Finally, the nature of CAN-BUS networks dictates that messages transmitted with the highest frequency are usually the ones trusted. This is another feature to protect against data corruption that can be exploited by attackers. If an attacker can transmit a replay a particular type of data more often than the legitimate sensor is transmitting it, other devices on the network will likely use the attacker's replayed data rather than the legitimate data.

## Demonstration

To execute your own replay attack first set up your plant device on the network and initialize the CAN interface. &#x20;

Once your CAN interface is initialized and you can read traffic, start a candump.

```
candump can0 -l
```

Now make some kind of change to the vessel state that you'd like to recreate through the execution of the replay attack.  Depending on your vessel this may include things like turning lights on or off, changing the rudder position, or changing the propulsion.

Once you've made your desired changes immediately stop the candump.  It's best practice to avoid capturing unnecessary data when completing a replay attack to try in order to try and isolate only the desired changes. &#x20;

Now reset your vessel back to its original state, before you made any changes to its state.  This is necessary to determine if the replay attack was successful upon execution.

At this point you're ready to replay the log file, which can be done using:

```
canplayer -I <candump_filename.log>
```

If your vessel recreates the actions that you performed, then that means your replay attack was successful!

If your vessel did not recreate the desired actions, make sure that what you're looking to recreate involves some form of NMEA2000 communication and that that communication is seen taking place on the bus.
