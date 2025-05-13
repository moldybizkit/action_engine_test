from errors.base_error import BaseError


# Description: Custom errors for the service layer
class ServiceError(BaseError):
    pass


class CityNotFoundError(ServiceError):
    def __init__(self, city: str):
        super().__init__(f"City '{city}' not found in the configuration.")


class ClientError(ServiceError):
    def __init__(
        self,
        message: str = "An error occurred while communicating with the weather client",
        details: str = None,
    ):
        super().__init__(message)
        self.details = details
        
    def to_dict(self):
        base_dict = super().to_dict()
        if self.details:
            base_dict["details"] = self.details
            
        return base_dict

class UnexpectedError(ServiceError):
    def __init__(self, message: str = "An unexpected error occurred"):
        super().__init__(message)
