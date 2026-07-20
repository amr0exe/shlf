from rest_framework.views import exception_handler
from rest_framework import status
from utils.responses import StdResponse

def std_exception_handler(exc, context):
    """
    Intercept any validation, db, or system errors project-wide
    """
    response = exception_handler(exc, context)

    if response is not None:
        return StdResponse(
            success=False,
            message="Validation or resource error encountered.",
            data=response.data,
            status_code=response.status_code
        )
    else:
        return StdResponse(
            success=False,
            message="An unexpected critical server error occured",
            data={"detail": str(exc)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
