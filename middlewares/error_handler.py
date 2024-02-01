"""
A "middleware" is a function that works with every request before it is processed by any specific path operation. 
And also with every response before returning it.

So we can handle errors efficiently by providing more meaningful error info.
"""

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, dispatch: DispatchFunction | None = None) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | HTTPException:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                content=str(e))


