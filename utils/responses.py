from rest_framework.response import Response
from rest_framework import status

class StdResponse(Response):
    """
    An extension to DRF's response, enforcing predicable structure
    """
    def __init__(self, data=None, message="Operation successful.", success=True, status_code=status.HTTP_200_OK, **kwargs):
        enveloped_data = {
            "success": success,
            "message": message,
            "data": data if data is not None else {}
        }
        super().__init__(data=enveloped_data, status=status_code, **kwargs)
