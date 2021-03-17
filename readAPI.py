import requests

response = requests.get("https://api.github.com/users/Matan")
print(response.status_code)

