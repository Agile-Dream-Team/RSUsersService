from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/webhooks")
async def receive_webhook(request: Request):
    data = await request.json()
    print(data)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Webhook received"})
