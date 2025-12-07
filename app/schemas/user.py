from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    role: str

    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    full_name: str | None = None
