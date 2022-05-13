from typing import Optional
from pydantic import BaseModel


class VerifyBase(BaseModel):
    email: str


class VerifyResponse(VerifyBase):
    user: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    disposable: Optional[bool] = False
