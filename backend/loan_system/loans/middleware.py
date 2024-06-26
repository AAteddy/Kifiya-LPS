# import logging
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from rest_framework.views import exception_handler as drf_exception_handler
# from .exceptions import BusinessRuleViolation, ExternalServiceError, LoanValidationError

# logger = logging.getLogger(__name__)


# def custom_exception_handler(exc, context):
#     response = drf_exception_handler(exc, context)

#     if response is not None:
#         return response

#     if isinstance(exc, ObjectDoesNotExist):
#         return JsonResponse({"error": "Resource not found."}, status=404)

#     if isinstance(exc, ValidationError):
#         return JsonResponse({"error": exc.message}, status=400)

#     if isinstance(exc, LoanValidationError):
#         return JsonResponse({"error": exc.detail}, status=exc.status_code)

#     if isinstance(exc, BusinessRuleViolation):
#         return JsonResponse({"error": exc.detail}, status=exc.status_code)

#     if isinstance(exc, ExternalServiceError):
#         return JsonResponse({"error": exc.detail}, status=exc.status_code)

#     logger.error("Unhandled exception: %s", str(exc), exc_info=True)
#     return JsonResponse({"error": "An unexpected error occurred."}, status=500)


# class ExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_exception(self, request, exception):
#         logger.error("Unhandled exception: %s", str(exception), exc_info=True)
#         response = custom_exception_handler(exception, None)
#         return response
