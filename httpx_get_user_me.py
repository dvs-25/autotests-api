import httpx  # Импортируем библиотеку HTTPX

# Данные для входа в систему
login_payload = {
    "email": "John@example.com",
    "password": "1234"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}

client = httpx.Client(headers=user_headers)

me_response = client.get("http://localhost:8000/api/v1/users/me")
me_response_data = me_response.json()

print("Me response:", me_response_data)
print("Status Code:", me_response.status_code)
client.close()