from logger import logger
class ExitException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ExpiredException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CredentialsException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ClientException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ServerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)    


class InternalServerError(Exception)        :
    def __init__(self, message: str) -> None:
        logger.error(message)
        super().__init__(message)    
class AlreadyExistsError(Exception)        :
    def __init__(self, message: str) -> None:
        super().__init__(message)    

class DoesNotExistsError(Exception)        :
    def __init__(self, message: str) -> None:
        super().__init__(message)    
