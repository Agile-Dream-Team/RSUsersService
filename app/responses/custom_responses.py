from fastapi.responses import JSONResponse


class CustomResponse(JSONResponse):
    def __init__(self, content: dict, status_code: int = 200):
        super().__init__(content=content, status_code=status_code)


class SuccessResponse(CustomResponse):
    def __init__(self, data: dict):
        content = {"status": "success", "data": data}
        super().__init__(content=content, status_code=200)


class ErrorResponse(CustomResponse):
    def __init__(self, error: str, status_code: int):
        content = {"status": "error", "error": error}
        super().__init__(content=content, status_code=status_code)
