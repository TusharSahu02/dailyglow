from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.controllers import log_controller
from app.utils.logger import logger
from sentry_sdk import capture_exception
from app.utils.settings import SENTRY_DSN
import sentry_sdk

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,  # 100% performance monitoring (optional, tweak later)
    environment="development",  # or "production"
    send_default_pii=True,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
)

app = FastAPI(title="Dailyglow")

# Register Routers
app.include_router(log_controller.router)


# Global Exception Handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation Error",
            "details": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail, "details": None},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {exc}")
    capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error",
            "details": str(exc),
        },
    )
