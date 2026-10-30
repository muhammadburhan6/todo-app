"""Request and response shapes for authentication routes."""

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=6, examples=["secretpassword"])
    display_name: str = Field(default="User", examples=["John Doe"])


class AuthResponse(BaseModel):
    uid: str
    email: str
    token: str
    message: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=6, examples=["secretpassword"])
