from rest_framework.exceptions import APIException


class LoanApplicationNotFound(APIException):
    status_code = 404
    default_detail = "Loan application not found."


class InvalidLoanStatus(APIException):
    status_code = 400
    default_detail = "Invalid loan status for this operation."


class LoanValidationError(APIException):
    status_code = 400
    default_detail = "Loan validation failed."
