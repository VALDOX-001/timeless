from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
from routes import (actorRoute,
                    directorRoute, priceRoute, seatRoute, ticketRoute, playRoute, customerRoute, showtimeRoute)
from routes.auth import auth_router

# 🔐 Auth Config
SECRET_KEY = "LUCT"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 🔥 FastAPI App
app = FastAPI()

# 🌐 CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Register Routes
app.include_router(auth_router)
app.include_router(actorRoute.actor_router)
app.include_router(directorRoute.director_router)
app.include_router(playRoute.play_router)
app.include_router(customerRoute.customer_router)
app.include_router(showtimeRoute.showtime_router)
app.include_router(seatRoute.seat_router)
app.include_router(ticketRoute.ticket_router)
app.include_router(priceRoute.price_router)

@app.get("/")
def root():
    return {"message": "🎭 Welcome to Sierra Leone Theatre"}

# 🔐 Get Current User From Token
def get_current_user_for_docs(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# 🎨 Custom OpenAPI with role-aware docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Fetch current user for role check
    try:
        from fastapi.requests import Request
        from starlette.testclient import TestClient
        client = TestClient(app)
        token_response = client.post("/auth/login", data={"username": "your_user", "password": "your_pass"})
        token = token_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        current_user = get_current_user_for_docs(token, next(get_db()))

    except:
        current_user = None  # For unauthenticated users

    openapi_schema = get_openapi(
        title="Sierra Leone Music Api",
        version="1.0.0",
        description="API with OAuth2 authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            },
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    # 👤 Hide non-GET methods for customer
    if current_user and current_user.role == "customer":
        for path in openapi_schema["paths"].values():
            methods_to_remove = [method for method in list(path.keys()) if method.lower() != "get"]
            for method in methods_to_remove:
                path.pop(method)

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
