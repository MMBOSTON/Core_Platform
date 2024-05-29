from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("myapp")

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail

async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"CustomException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

def setup_exception_handlers(app):
    app.add_exception_handler(CustomException, custom_exception_handler)
