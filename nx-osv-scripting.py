import requests
import json
target = 'https://10.10.11.2/ins'
username = input('Switchusername is: ')
password = input('Switch password is: ')
requestheaders = {"content-type":"application/json"}
showcmd = {
    "ins_api": {
        "version":"1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid":"1",
        "input":"show ip interface brief",
        "output_format": "json",
    }
}
response = requests.post(
    target,
    data=json.dumps(showcmd),
    headers=requestheaders,
    auth=(username,password),
    verify=False
).json()
print(json.dumps(response, indent=2, sort_keys=True))
