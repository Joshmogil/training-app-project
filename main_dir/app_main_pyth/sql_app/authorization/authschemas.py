from pydantic import BaseModel

class AuthDetails(BaseModel):
    email: str
    password: str

class RegisterDetails(BaseModel):
    email: str
    password: str
    confirmPassword: str

