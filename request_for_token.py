import requests
import Remainder.settings as setting
data = {
    'grant_type': 'password',
    'username': 'admin',
    'password': 'root',
}

data_patch = {
    'status_todo' : False
}

response = requests.post('http://127.0.0.1:8000/o/token/', data=data, auth=(setting.REMAINDER_KEY,setting.REMAINDER_SECRET))
# response = requests.get('http://127.0.0.1:8000/api/v1/task', headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})
# response = requests.patch('http://127.0.0.1:8000/api/v1/task/1',data=data_patch, headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})

print(response.status_code)
print(response.json())