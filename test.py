import requests
from datetime import datetime

print(requests.get("http://127.0.0.1:8000/").json())

print("Adding an item")
print(requests.post(
        "http://127.0.0.1:8000/",
        json={"filename": "cat5.jpeg", "contentType": "image/jpeg", "createdDate": int(datetime.now().timestamp())}
    )
)
print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Updating an item")
print(requests.put("http://127.0.0.1:8000/image/0?filename=cat9.jpeg").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Deleting an item")
print(requests.delete("http://127.0.0.1:8000/image/0").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()
