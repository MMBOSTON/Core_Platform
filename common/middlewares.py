"""
bettter docstring needed...
common middlewares.py for authentication and HTTP request handling

"""
import logging

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from auth.jwt_handler import verify_token  # Ensure this is correctly implemented

class VerifyJWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in ["/login", "/register"]:
            token = request.headers.get("Authorization")
            if token:
                token = token.split(" ")[1]
                payload = verify_token(token)
                if payload is None:
                    raise HTTPException(status_code=403, detail="Invalid token")
        response = await call_next(request)
        return response

def setup_common_middlewares(app):
    app.add_middleware(VerifyJWTMiddleware)
    logger = logging.getLogger(__name__)
    logger.info("Common Middlewares imported successfully.")

