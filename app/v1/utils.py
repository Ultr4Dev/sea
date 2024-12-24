import http
from http.client import HTTPException
import random
import string

import fastapi

import fastapi.exceptions
import sqlalchemy
import sqlalchemy.exc
from fastapi import HTTPException, Request


def random_string(n=8, prefix="") -> str:

    return prefix + "".join(random.choices(string.ascii_letters + string.digits, k=n))


class StatusCheckMiddleware:
    def __init__(
        self,
        app,
    ):
        self.app = app

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        if request.url.path == "/health":
            return await call_next(request)
        if self.app.operational is False:
            print("Service is down")
            raise HTTPException(
                status_code=http.HTTPStatus.SERVICE_UNAVAILABLE,
                detail="Service is down",
            )
        print("Service is up")
        # process the request and get the response
        response = await call_next(request)

        return response


class ExceptionHandler:
    def __init__(self):
        self.operational = True

    def exception_handler(self, exception) -> fastapi.responses.JSONResponse:
        if isinstance(exception, sqlalchemy.exc.PendingRollbackError):

            return fastapi.responses.JSONResponse(
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Database error",
                    "status": http.HTTPStatus.INTERNAL_SERVER_ERROR,
                },
            )
        if isinstance(exception, HTTPException):
            if exception.status_code not in http.HTTPStatus.__members__.values():
                raise exception
            return fastapi.responses.JSONResponse(
                content={
                    "detail": exception.detail,
                    "status": exception.status_code,
                },
                status_code=exception.status_code,
            )

        else:
            self.operational = False
            return fastapi.responses.JSONResponse(
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "status": http.HTTPStatus.INTERNAL_SERVER_ERROR,
                },
            )
