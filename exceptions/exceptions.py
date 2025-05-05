from fastapi import HTTPException

class ApiException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"X-Error-Code": error_code}
        )

class BookAlreadyExists(ApiException):
    def __init__(self):
        super().__init__(
            status_code = 404,
            detail = "Le livre existe déjà dans la db!",
            error_code = "BOOK_ALREADY_EXISTS"
        )

    
    

