class BookAlreadyExists(Exception):
    def __init__(self, message, error_code):
        super().__init__()
        self.error_code = error_code
        self.message = message
    
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"    