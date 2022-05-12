from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.v1 import api as api_v1

app = FastAPI()

app.include_router(api_v1.router, prefix="/api/v1")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")