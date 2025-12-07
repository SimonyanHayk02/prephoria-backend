from pydantic import BaseModel, EmailStr, model_validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    full_name: str | None = None

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str
