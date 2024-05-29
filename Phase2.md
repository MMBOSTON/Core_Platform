Sure, here is the continuation of the [README.md](http://README.md) for Phase 2.

markdown

Copy code

`create_all(bind=engine)  dictConfig(LOGGING_CONFIG)  app = FastAPI()  def get_db():     db = SessionLocal()     try:         yield db     finally:         db.close()  app.include_router(user_routers.router)  @app.middleware("http") async def verify_jwt_middleware(request: Request, call_next):     if request.url.path not in ["/login", "/register"]:         token = request.headers.get("Authorization")         if token:             token = token.split(" ")[1]             payload = verify_token(token)             if payload is None:                 raise HTTPException(status_code=403, detail="Invalid token")     response = await call_next(request)     return response app.middleware("http")(handle_exceptions)  if __name__ == "__main__":     import uvicorn     uvicorn.run(app, host="0.0.0.0", port=8000)`

### [models.py](http://models.py)

No changes needed in `models.py` from Phase 1, but ensure your file looks similar to this for reference:

python

Copy code

`from sqlalchemy import Column, Integer, String from common.database import Base  class User(Base):     __tablename__ = "users"      id = Column(Integer, primary_key=True, index=True)     username = Column(String, unique=True, index=True)     password = Column(String)     hashed_password = Column(String)`

### [schemas.py](http://schemas.py)

Enhance your schemas to include data validation:

python

Copy code

`from pydantic import BaseModel, Field  class UserBase(BaseModel):     username: str = Field(..., max_length=100)     password: str = Field(..., min_length=6, max_length=100)  class UserCreate(UserBase):     pass  class UserResponse(BaseModel):     id: int     username: str      class Config:         orm_mode: True`

### [exceptions.py](http://exceptions.py)

Create a custom exception handler:

python

Copy code

`from fastapi import Request, HTTPException from fastapi.responses import JSONResponse from sqlalchemy.exc import SQLAlchemyError import logging  logger = logging.getLogger(__name__)  async def handle_exceptions(request: Request, call_next):     try:         response = await call_next(request)     except HTTPException as exc:         return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})     except SQLAlchemyError as exc:         logger.error(f"Database error: {exc}")         return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})     except Exception as exc:         logger.error(f"Unexpected error: {exc}")         return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})     return response`

### logging\_config.py

Configure logging for your application:

python

Copy code

`LOGGING_CONFIG = {     "version": 1,     "disable_existing_loggers": False,     "formatters": {         "default": {             "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",         },     },     "handlers": {         "default": {             "level": "INFO",             "formatter": "default",             "class": "logging.StreamHandler",         },     },     "root": {         "level": "INFO",         "handlers": ["default"],     }, }`

### [middlewares.py](http://middlewares.py)

Create middleware for handling exceptions:

python

Copy code

`from fastapi import Request, HTTPException from fastapi.responses import JSONResponse import logging  logger = logging.getLogger(__name__)  async def handle_exceptions(request: Request, call_next):     try:         response = await call_next(request)     except HTTPException as exc:         return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})     except Exception as exc:         logger.error(f"Unexpected error: {exc}")         return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})     return response`

Testing the Application
-----------------------

1.  **Run the Application**
    
    Start your FastAPI application:
    
    bash
    
    Copy code
    
    `uvicorn main:app --reload`
    
2.  **Test the Endpoints**
    
    *   **Register User**: Send a POST request to `/users/register` with JSON body:
        
        json
        
        Copy code
        
        `{     "username" : "testuser" ,     "password" : "testpassword" }`
        
    *   **Login User**: Send a POST request to `/users/login` with JSON body:
        
        json
        
        Copy code
        
        `{     "username" : "testuser" ,     "password" : "testpassword" }`
        
    *   **Protected Endpoint**: Try accessing a protected endpoint (e.g., `/users/me`) with the Authorization header set to `Bearer <your_jwt_token>`.
        
3.  **Verify Logging and Error Handling**
    
    *   Check the console logs to ensure that all actions are being logged correctly.
    *   Induce errors (e.g., database errors, invalid inputs) and verify that they are handled gracefully with appropriate error messages returned to the client.

Conclusion
----------

In Phase 2, we have enhanced our FastAPI application with robust data validation, error handling, and logging mechanisms. These improvements ensure that our application is more resilient, secure, and easier to debug and maintain. Continue testing and refining your application as you progress to further phases.

* * *

This [README.md](http://README.md) should provide a comprehensive guide to implementing Phase 2 enhancements and verifying their functionality in your FastAPI project.