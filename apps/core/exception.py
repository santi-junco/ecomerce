from rest_framework.exceptions import APIException

class CustomException(APIException):
    status_code = 400
    default_detail = "Ocurrio un ERROR"
    default_code = 'ERROR'

    def __init__(self, error='Error al procesar la solicitud', code=400):
        self.default_detail = error
        self.status_code = code
        super().__init__()