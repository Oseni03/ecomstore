import requests
from getpass import getpass

# endpoint = "http://localhost:8000/api/product/create/"
auth_endpoint = "http://localhost:8000/api/auth/"

username = input("What is your username?\n")
password = getpass("What is your password?\n")

data = {
  "username": username,
  "password": password,
}
auth_response = requests.post(auth_endpoint, json=data)

if auth_response.status_code == 200:
  token = auth_response.json()["token"]
  
  headers = {
    "Authorization": f"Bearer {token}",
  }
  
  endpoint = "http://localhost:8000/api/product/"
  
  response = requests.get(endpoint, headers=headers)
  print(response.json())
  print(response.status_code)