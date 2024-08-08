from pydantic import BaseModel


class SuccessModel(BaseModel):
    status: str = "success"
    data: dict


class ErrorModel(BaseModel):
    status: str = "error"
    error: str
