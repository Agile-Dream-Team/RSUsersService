from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.v1.webhooks.webhook_routes import router as webhook_router

app = FastAPI()


class HealthCheck(BaseModel):
    status: str = "OK"
    msg: str = "Hello world"


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    return HealthCheck()


# Include the webhook routes under /api/v1
app.include_router(webhook_router, prefix="/api/v1")
