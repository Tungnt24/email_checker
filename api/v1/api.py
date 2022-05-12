from fastapi import APIRouter
from .endpoints import verify

router = APIRouter()

router.include_router(verify.router, tags=["verify"])
