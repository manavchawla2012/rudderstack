from rest_framework import status
from rest_framework.exceptions import ErrorDetail, APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response


def extract_message_from_data(data: [dict, list, tuple]):
    match type(data).__qualname__:
        case ErrorDetail.__qualname__:
            return str(data), data.code
        case list.__qualname__ | tuple.__qualname__:
            return extract_message_from_data(data[0])
        case str.__qualname__:
            return data, "request_failed"
        case _:
            return "error_not_found", "request_failed"


def extract_message_code_from_exception(response: dict | list):
    if type(response) == list:
        return extract_message_from_data(response[0])
    else:
        for key in response:
            return extract_message_from_data(response[key])


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response_data = response.data
        message, code = extract_message_code_from_exception(response.data)
        response.data = {
            "error": {
                "data": response_data,
                "message": message,
                "code": code,
            }
        }
    return response


class CustomApiException(APIException):
    detail = None
    status_code = None

    # create constructor
    def __init__(self, message=None, status_code=None):
        # override public fields
        CustomApiException.status_code = status_code or status.HTTP_400_BAD_REQUEST
        CustomApiException.detail = message


class VerificationMailSentException(CustomApiException):
    pass


class AccountAlreadyVerifiedException(CustomApiException):
    pass


class VerificationTokenException(CustomApiException):
    pass


class UserBusinessNotFoundException(CustomApiException):
    pass


class PGOrderCreationFailed(CustomApiException):
    pass


class PGInvalidVerificationResponse(CustomApiException):
    pass


class TokenNotFoundException(CustomApiException):

    def __init__(self, *args, **kwargs):
        kwargs["message"] = kwargs.get("message", "Token Not Found")
        super(TokenNotFoundException, self).__init__(*args, **kwargs)
