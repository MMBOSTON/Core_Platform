from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from auth.jwt_handler import verify_token
import logging

logger = logging.getLogger("myapp")

class VerifyJWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in ["/login", "/register"]:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=403, detail="Authorization header missing")
            try:
                token = token.split(" ")[1]
                payload = verify_token(token)  # Replace with your actual token verification logic
                if payload is None:
                    raise HTTPException(status_code=403, detail="Invalid token")
            except Exception as e:
                logger.error(f"Token verification error: {str(e)}")
                return JSONResponse(status_code=403, content={"detail": "Invalid token"})
        response = await call_next(request)
        return response

def setup_middlewares(app):
    app.add_middleware(VerifyJWTMiddleware)
