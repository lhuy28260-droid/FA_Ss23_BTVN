from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# AUTH
# ==========================================

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================================
# USER
# ==========================================

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# RESOURCE
# ==========================================

class ResourceCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150
    )

    description: str | None = None


class ResourceUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    description: str | None = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )