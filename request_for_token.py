import requests
import Remainder.settings as setting
data = {
    'grant_type': 'password',
    'username': 'admin',
    'password': 'root',
}

response = requests.post('http://127.0.0.1:8000/o/token/', data=data, auth=(setting.REMAINDER_KEY,setting.REMAINDER_SECRET))


print(response.status_code)
print(response.json())

