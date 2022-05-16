from fastapi import APIRouter
from .endpoints import verification

router = APIRouter()

router.include_router(verification.router, tags=["verification"])
