import requests
import json

url = "https://10.10.11.2/api/aaaLogin.json"

payload = json.dumps({
  "aaaUser": {
    "name": "admin",
    "pwd": "WE#2020@esp"
  }
})
headers = {
  'Content-Type': 'application/json',
  'x-auth-token': '{{token}}',
  'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA=='
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
