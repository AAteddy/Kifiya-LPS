from .models import LoanApplication, LoanRepayment
from django.utils import timezone


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
    loan_application.status = "Approved"
    loan_application.approved_at = timezone.now()
    loan_application.save()
