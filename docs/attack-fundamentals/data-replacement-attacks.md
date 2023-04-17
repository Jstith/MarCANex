---
description: Attacking CAN-BUS protocol at the physical layer
---

# Data Replacement Attacks

## What is a Data Replacement Attack

So far, every attack discussed involves either creating our own data from scratch or replaying data from a legitimate source. However, these attacks have a weakness: They still have to contest with legitimate data coming from legitimate devices at the same time. Data replacement attacks are the next level in which attackers change the data as it is being transmitted in the network. When properly executed, this style of attack is incredibly powerful for many reasons, including:

* There is no conflict between legitimate messages and spoofed/replayed messages
* Metadata of source devices can be preserved
* The natural frequency of transmission is preserved
* This type of attack is **very, very hard to detect**.

## Data Replacement Attacks on NMEA 2000 Networks

Data replacement attacks are possible on NMEA 2000 networks due to the inherent design choices of a broadcast based network. In order for arbitration to work on a CAN-BUS network, data is broadcasted at an agreed on speed. For NMEA 2000, this speed is 250,000 samples per second. This means that during any period of time between each sample, changes to the state of the broadcast wire go un-noticed by the devices who all agreed to sample at a certain time. So, if a device is fast enough, it can read the data between the agreed on sample times, and make changes to it before the other devices on the network read the data being sent (electrons move very quickly).

### Another Explanation

Imagine you are in a room full of people, and everyone in the room has their own custom light switch. Anyone in the room can turn on the lights, or turn them off, at any time using their light switch (power and ground on the wire). To make sure everyone is on the same page about what constitutes "on" and "off" for the light, everyone in the room decides to close their eyes and blink open every 5 seconds, at which point they will record if the light is on or off. If someone wants to turn on or off the light, they can do so with their personal light switch. However, one person decides to cheat. The cheater opens their eyes after 4 seconds, checks if the light is on or off, and changes it with their light switch before everyone else opens their eyes.

This is the essence of how data replacement attacks work on a CAN-BUS broadcast based network. It requires a very fast tool to sample the data on the bus at a quicker rate than the one other devices agree on, and has the ability to change that data. The CANT board developed by Grimm Cybersecurity R\&D does just that.

Using data replacement attacks, any data send over the NMEA 2000 network is vulnerable to being changed mid-transmission, undenounced to the other devices on the network. The possibilities of this attack are only limited by what devices communicate on the network. On new ships, this can include everything from the rudder to the propeller. On Coast Guard small boats, this includes all navigation, radar, radio, and AIS sensors and transmitters.

