"""
setup_chd_middlewares function to add CHD middleware to FastAPI app.
"""

# customer_health_dashboard/chd_middlewares.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class ChdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Add any dashboard-specific middleware logic here
        # For example, logging, rate limiting, etc.
        response = await call_next(request)
        return response

def setup_chd_middlewares(app):
    app.add_middleware(ChdMiddleware)
