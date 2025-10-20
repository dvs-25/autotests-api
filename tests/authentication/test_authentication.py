from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema, \
    RefreshResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response, assert_refresh_response, \
    assert_invalid_token_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    @allure.story(AllureStory.LOGIN)
    @allure.title("Login with correct email and password")
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        request = LoginRequestSchema(email=function_user.email, password=function_user.password)
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.LOGIN)
    @allure.title("Refresh token")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_refresh_token(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        login_request = LoginRequestSchema(email=function_user.email, password=function_user.password)
        login_response = authentication_client.login_api(login_request)
        login_response_data = LoginResponseSchema.model_validate_json(login_response.text)
        request = RefreshRequestSchema(refreshToken=login_response_data.token.refresh_token)
        response = authentication_client.refresh_api(request)
        response_data = RefreshResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_refresh_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.LOGIN)
    @allure.title("Invalid refresh token")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_invalid_refresh_token(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        request = RefreshRequestSchema()
        response = authentication_client.refresh_api(request)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_invalid_token_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
