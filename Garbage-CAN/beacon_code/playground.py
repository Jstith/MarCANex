import json

input_data = '{"ip": "0.0.0.0", "port": 4000, "message": "INIT?"}'
js = json.loads(input_data)

print(js['message'])