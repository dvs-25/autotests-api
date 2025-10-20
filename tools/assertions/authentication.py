import allure

from clients.authentication.authentication_schema import LoginResponseSchema, RefreshResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
from tools.assertions.errors import assert_internal_error_response
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("AUTHENTICATION_ASSERTIONS")


@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    """
    Проверяет корректность ответа при успешной авторизации.

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info("Check login response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


@allure.step("Check refresh token response")
def assert_refresh_response(response: RefreshResponseSchema):
    """
    Проверяет корректность ответа при успешном обновлении токена.

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info("Check refresh token response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


@allure.step("Check invalid or expired refresh token response")
def assert_invalid_token_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если передать невалидный токен.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Invalid or expired refresh token"
    """
    logger.info("Check user not found response")
    expected = InternalErrorResponseSchema(details="Invalid or expired refresh token")
    assert_internal_error_response(actual, expected)
