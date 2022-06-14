import requests

res = requests.post("https://notify-api.line.me/api/notify",headers={'Authorization': 'Bearer VaQiVzn5SqjJysdYSblOaJuS5xCBDw3qucIfzmJPyI5'},data={"message":"TEST"})
print(res.status_code)
