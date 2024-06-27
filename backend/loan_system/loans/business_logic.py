# business_logic.py

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
