import requests

# endpoint = "http://localhost:8000/api/product/create/"
endpoint = "http://localhost:8000/api/category/create/"


data = {
  "name": "New Shoe",
  "slug": "new-shoe",
}
response = requests.post(endpoint)
print(response.json())
print(response.status_code)