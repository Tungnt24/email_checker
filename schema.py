from typing import Optional
from pydantic import BaseModel


class Verify(BaseModel):
    email: str
    user: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    disposable: Optional[bool] = None