from rest_framework.response import Response
from rest_framework import status
from typing import Any


def success_response(status=status.HTTP_200_OK, message="Success", data=None):
    return Response({"data": data or {}, "message": message}, status=status)


def error_response(
    status: int=status.HTTP_400_BAD_REQUEST, message: str="Error occurred", errors: Any=None
) -> Response:
    data: dict[str, str | list | dict] = {"message": message}
    if errors is not None:
        if isinstance(errors, dict):
            data["errors"] = errors
        elif isinstance(errors, (list, tuple)):
            data["errors"] = list(errors)
        else:
            data["errors"] = [str(errors)]
    return Response(data, status=status)
