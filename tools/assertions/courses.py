import allure

from clients.courses.courses_schema import CourseSchema, UpdateCourseRequestSchema, UpdateCourseResponseSchema, \
    GetCoursesResponseSchema, CreateCourseResponseSchema, CreateCourseRequestSchema, GetCourseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response, assert_validation_error_response
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user
from tools.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")


@allure.step("Check update course response")
def assert_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema
):
    """
    Проверяет, что ответ на обновление курса соответствует запросу.

    :param request: Исходный запрос на обновление курса.
    :param response: Ответ API с данными курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check update course response")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check course")
def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check course")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


@allure.step("Check get courses response")
def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[CreateCourseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные пользователя не совпадают.
    """
    logger.info("Check get courses response")
    assert_length(get_courses_response.courses, create_course_responses, "courses")

    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)


@allure.step("Check create course response")
def assert_create_course_response(
        request: CreateCourseRequestSchema,
        response: CreateCourseResponseSchema
):
    """
    Проверяет, что ответ на создание курса соответствует запросу.

    :param request: Исходный запрос на создание курса.
    :param response: Ответ API с данными курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check create course response")
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(
        response.course.preview_file.id,
        request.preview_file_id,
        "preview_file_id"
    )
    assert_equal(
        response.course.created_by_user.id,
        request.created_by_user_id,
        "created_by_user_id"
    )


@allure.step("Check get course response")
def assert_get_course_response(
        get_course_response: GetCourseResponseSchema,
        create_course_response: CreateCourseResponseSchema
):
    """
    Проверяет, что ответ на получение курса соответствует ответу на его создание.

    :param get_course_response: Ответ API при запросе данных курса.
    :param create_course_response: Ответ API при создании курса.
    :raises AssertionError: Если данные курса не совпадают.
    """
    logger.info("Check get course response")
    assert_course(get_course_response.course, create_course_response.course)


@allure.step("Check course not found response")
def assert_course_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если курс не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Course not found"
    """
    logger.info("Check file not found response")
    expected = InternalErrorResponseSchema(details="Course not found")
    assert_internal_error_response(actual, expected)


@allure.step("Check get course with incorrect course id response")
def assert_get_course_with_incorrect_course_id_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ API на запрос курса с некорректным course_id
    соответствует ожидаемому формату ошибки валидации.

    :param actual: Фактический ответ API с ошибкой валидации
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому
    """
    logger.info("Check get course with incorrect course id response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-course-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` "
                             "followed by [0-9a-fA-F-], found `i` at 1"
                },
                message="Input should be a valid UUID, invalid character: "
                        "expected an optional prefix of `urn:uuid:` "
                        "followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "course_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
