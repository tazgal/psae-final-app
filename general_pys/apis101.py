import requests

url_api = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(url_api)
response.json()
print(response.json())
