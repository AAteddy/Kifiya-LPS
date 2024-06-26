from .models import LoanApplication, LoanRepayment
from django.utils import timezone

# from .exceptions import LoanValidationError, BusinessRuleViolation, ExternalServiceError


# def validate_loan_application(loan_application):
#     errors = []
#     # Example validation checks
#     if loan_application.borrower.credit_score < 600:
#         errors.append("Credit score too low.")
#     if loan_application.amount > loan_application.borrower.annual_income * 0.5:
#         errors.append("Loan amount exceeds allowable limit based on income.")
#     if errors:
#         raise LoanValidationError(errors)
#     return errors


# def approve_loan(loan_application):
#     if loan_application.status != "Pending":
#         raise BusinessRuleViolation("Only pending loans can be approved.")
#     # Simulate external service check (mocked)
#     try:
#         external_check_result = True  # Replace with actual external check
#         if not external_check_result:
#             raise ExternalServiceError("External credit check failed.")
#     except Exception as e:
#         raise ExternalServiceError(str(e))
#     loan_application.status = "Approved"
#     loan_application.save()


# def disburse_loan(loan_application):
#     if loan_application.status != "Approved":
#         raise BusinessRuleViolation("Only approved loans can be disbursed.")
#     # Simulate disbursement process
#     loan_application.status = "Disbursed"
#     loan_application.save()


# def record_repayment(loan_application, amount):
#     if loan_application.status not in ["Approved", "Disbursed"]:
#         raise BusinessRuleViolation("Only approved or disbursed loans can be repaid.")
#     # Record the repayment (no actual money transfer simulation)
#     repayment = LoanRepayment(loan=loan_application, amount=amount)
#     repayment.save()


def validate_loan_application(loan_application):
    """Function to validate a loan application."""
    errors = []
    borrower = loan_application.borrower
    if borrower.credit_score < 600:
        errors.append("Credit score too low")
    if borrower.annual_income <= 0:
        errors.append("Invalid annual income")
    if borrower.debt_to_income_ratio > 0.4:
        errors.append("Debt to income ratio too high")
    return errors


def approve_loan(loan_application):
    """Function to approve a loan application."""
    loan_application.status = "Approved"
    loan_application.approved_at = timezone.now()
    loan_application.save()


def disburse_loan(loan_application):
    """Function to disburse a loan."""
    loan_application.status = "Disbursed"
    loan_application.disbursed_at = timezone.now()
    loan_application.save()


def record_repayment(loan_application, amount):
    """Function to record a loan repayment."""
    LoanRepayment.objects.create(loan=loan_application, amount=amount)
    # Here I can add more complex logic for calculating outstanding balance and interest.
