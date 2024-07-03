import requests
import json

url = "http://127.0.0.1:8000/api/register"

payload = json.dumps({
  "username": "erd",
  "password": "adasdfsdf",
  "chat_id": "sdfsdfsdf",
  "payment_status": 1,
  "payment_checkout_uri": "adsasdasdas",
  "payment_id": "scfsdfc"
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
