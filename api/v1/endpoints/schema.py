from typing import Optional
from pydantic import BaseModel


class VerificationBase(BaseModel):
    email: str


class VerificationResponse(VerificationBase):
    user: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    disposable: Optional[bool] = False
