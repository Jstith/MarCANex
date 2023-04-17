---
description: Exploiting the trust in CAN-BUS networks
---

# Denial of Service Attacks

## What is a Denial of Service Attack?

A denial of service (DOS) attack is a unique type of of attack that targets resource limitations. DOS attacks aim to flood a device, service, or network with so much traffic that things will either behave unpredictably or outright stop working because they are not prepared to handle the volume of traffic they receive. For example, if an attacker attempted to log in 1 million times a second to a webpage, the webserver might eventually run out of memory to process those requests and either dump an error message, or just not work for anyone else. Either result can be considered a successful DOS attack.

## Denial of Service on NMEA 2000

A DOS attack can be carried out against a NMEA 2000 network simply by flooding the bus with so much information the devices cannot receive and parse it all. Additionally, an attacker can connect power to a wire or ground a wire, essentially making all data on the bus either a 0 or a 1 respectively. However, there is a much cleaner way to simulate a denial of service attack on NMEA 2000 networks.

### Spoofing Based DOS Attack

As mentioned in the Marine Network Protocols section, CAN-BUS networks use an arbitration based system to determine the order in which messages get broadcasted to the network. To recap, each CAN message is assigned a number called its arbitration ID (arbid). The lower the arbid, the higher priority the message has. When a device desires to transmit a message, it will first listen on the bus for any other messages. If it hears a message with a lower (more important) arbid, it will wait until the message has fully transmitted before sending its own message. However, if the device sees a higher (less important) arbid, it will simple talk over it.

All devices on CAN-BUS networks agree to follow this set of rules regarding arbitration, and an attacker can exploit that to simulate a DOS attack using spoofed packets. All an attacker must do is generate a lot of traffic with an arbid of 0 (the most important possible message). The data doesn't have to mean anything, and can in fact just be all zeros or ones for simplicity. Rapidly sending this message effectively executes a DOS attack against the network, because all other devices will keep waiting to send their lower priority messages until the message with the higher priority is finished... except it never will be until the attacker stops the attack.

This simple but powerful hack against the NMEA 2000 network allows attackers to DOS a network without causing any permanent damage to wires or devices. The network can be turned off and back on, and the DOS will still execute. It is also very hard to differentiate this attack from a mechanical failure without the proper tools for analysis.

## Demonstration

We have traditionally executed this attack using the _cyber paperclip_ mode on the CANT board, but it can also be executed from a Linux system if your baud rate (speed of transmission) is set correctly.

```
while true
do
    cansend can0 000000#FFFFFFFFFFFFFFFF
done
```

