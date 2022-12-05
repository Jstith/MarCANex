import json

from cryptography.fernet import Fernet

with open('sym.key', 'rb') as f:
            sym_key = f.read()
            f.close()
            fernet = Fernet(sym_key)

data = {
    "message" : "PORT SET",
    "data" : "1338"
}

data2 = json.dumps(data)

print(fernet.encrypt(data2.encode()))
