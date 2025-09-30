from functools import lru_cache

from httpx import Client
from pydantic import BaseModel

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.event_hooks import curl_event_hook, log_request_event_hook, \
    log_response_event_hook  # Импортируем event hook
from config import settings

class AuthenticationUserSchema(BaseModel, frozen=True):
    email: str
    password: str


@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    authentication_client = get_authentication_client()

    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=settings.http_client.timeout,  # Используем значение таймаута из настроек
        base_url=settings.http_client.client_url,  # Используем значение адреса сервера из настроек
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],  # Логируем исходящие HTTP-запросы
            "response": [log_response_event_hook]  # Логируем полученные HTTP-ответы
        }
    )
