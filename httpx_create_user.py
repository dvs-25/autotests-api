import httpx
from tools.fakers import fake  # Импортируем функцию для генерации случайного email

payload = {
    "email": fake.email(),  # Используем функцию для генерации случайного email
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
response = httpx.post("http://localhost:8000/api/v1/users", json=payload)

print(response.status_code)
print(response.json())