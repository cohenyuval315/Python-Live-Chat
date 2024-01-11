class ErrorMessage(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)    
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