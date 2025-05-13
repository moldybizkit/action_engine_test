class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
    def to_dict(self):
        return {"message": self.message}