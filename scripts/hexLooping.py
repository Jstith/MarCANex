import os

import csv


os.system("echo > chaseTest3.txt")
os.system("echo > csvmaker.txt")

counter=0x0

f=open("csvmaker.txt","w")

for i in range(500):
    
    
    start = "0x000000"  # hex literal, gives us a regular integer
    plus = "FFFF0000FC"
    hex_string=start+plus
    hexStart=int(hex_string,16)
    
    
    hexStart = "{:06x}".format(i)
    hexx=hexStart + plus

    print(hexx)
    binn=bin(int(hexx, base=16)).lstrip('0b')
    
    print(binn)
    print(type(binn))
    os.system("echo >> chaseTest2.txt")
    command3="echo \""+ "{:034b}".format(int(binn)) + "\" >> chaseTest3.txt"
    command2="echo \"echo '(1664564348.469461) can0 09F8016E#" + hexx + "\" >> chaseTest3.txt"
    command="echo '(1664564348.469461) can0 09F1126E#" + hexx + "' | candump2analyzer|analyzer >> chaseTest3.txt"
    command4="echo '(1664564348.469461) can0 09F1126E#" + hexx + "' | candump2analyzer|analyzer"

    os.popen(command2)
    os.system(command)
    heyo = os.popen(command4).read()
    heading = heyo.split("=")[2]
   
    f.write("{:065b}".format(int(binn,2)) + " : " + heading + " : " + hexx + "\n" )

    f.write("\n")

    os.system("echo >> chaseTest2.txt")





with open('csvmaker.txt', mode ='r')as file: 
      
  # reading the CSV file 
  csvFile = csv.reader(file) 
    
  # displaying the contents of the CSV file 
  for lines in csvFile: 
        print(lines) 