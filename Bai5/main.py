from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from middleware.request_middleware import RequestMiddleware
from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.resource_router import router as resource_router

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="Secure Learning Portal",
    description="Secure API for learning resources",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PATCH",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Authorization",
        "Content-Type"
    ],
)


# ==========================================
# CUSTOM MIDDLEWARE
# ==========================================

app.add_middleware(
    RequestMiddleware
)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(resource_router)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get(
    "/health",
    tags=["System"]
)
def health_check():
    return {
        "status": "ok",
        "message": "Secure Learning Portal is running"
    }