""" module for custom exceptions """
class BaseHTTPException(Exception):
    status_code: int
    detail: str

    def __init__(self, status_code: int, error_code: str, detail: str):
        self.status_code = status_code  # http
        self.error_code = error_code  # to frontend handler
        self.detail = detail

class InvalidInputException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422, error_code='InvalidInput',detail=detail)

class FileNotFoundException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, error_code='FileNotFound', detail=detail)

class PostNotFoundException(BaseHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, error_code='PostNotFound', detail=detail)

# TODO: add detailed error messages, diagnostic information,
# logging, and thorough testing
