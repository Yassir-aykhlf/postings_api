from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

_STATUS_CODE_NAMES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    422: "validation_error",
    429: "rate_limited"
}

def error_envelope(code: str, message: str, fields: dict[str, str] | None = None) -> dict:
    error: dict[str, Any] = {"code": code, "message": message}
    if fields is not None:
        error["fields"] = fields
    return {"error": error}

class AppError(Exception):
    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str, *, fields: dict[str, str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.fields = fields

class NotFoundError(AppError):
    status_code = 404
    code = "not_found"

class ConflictError(AppError):
    status_code = 409
    code = "conflict"

class ValidationError(AppError):
    status_code = 422
    code = "validation_error"

class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"

class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"

def _remap_validation(exc: RequestValidationError) -> dict[str, str]:
    fields: dict[str, str] = {}
    for err in exc.errors():
        path = [str(p) for p in err["loc"] if p not in ("body", "query", "path", "header")]
        key = ".".join(path) if path else "__root__"
        fields[key] = err["msg"]
    return fields

def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse (
            status_code=exc.status_code,
            content=error_envelope(exc.code, exc.message, exc.fields)
        )
    @app.exception_handler(RequestValidationError)
    async def _handle_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_envelope(
                "validation_error", "Request validation failed", _remap_validation(exc)
            )
        )
    @app.exception_handler(StarletteHTTPException)
    async def _handle_http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = _STATUS_CODE_NAMES.get(exc.status_code, "http_error")
        message = exc.detail if isinstance(exc.detail, str) else code
        return JSONResponse(status_code=exc.status_code, content=error_envelope(code, message))