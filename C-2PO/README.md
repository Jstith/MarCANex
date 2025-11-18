# C-2PO: Command and Control for Protocols Offshore

**CURRENLTY UNDER DEVELOPMENT**

## Beacon Node

### Install

To install the C-2PO Beacon, begin by updating and installing the necessary packages for python, pip, python virtual environment (venv), and git. The installation steps for Debian-based package management is shown below:

```
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv
```

Next, clone the GitHub repository:

```
git clone git@github.com:Jstith/C-2PO.git
```

Once you've cloned the repository, cd into the directory and set up your python virtual environment:

```
cd C-2PO/beacon
```

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```

Install the python dependencies using the requirements.txt file:

```
pip install -r requirements.txt
```

Finally, run the beacon.py script with the help flag to see options to configure your beacon:

```
python3 beacon.py -h
usage: beacon.py [-h] [--ip IP] [--port PORT] [--lport LPORT] [--bind BIND]

options:
  -h, --help     show this help message and exit
  --ip IP        Remote IP of C2 server (default 127.0.0.1)
  --port PORT    Initialization port of C2 server (default 2023)
  --lport LPORT  Local listening port (default 4000)
  --bind BIND    Local listen interface (default 0.0.0.0)

```

### Pip Requirements

```
cffi==1.15.1
cryptography==38.0.3
msgpack==1.0.4
packaging==21.3
pycparser==2.21
pyparsing==3.0.9
python-can==4.0.0
termcolor==2.1.0
typing_extensions==4.4.0
wrapt==1.14.1
```

## Hive Node

### Install

### Requirements
