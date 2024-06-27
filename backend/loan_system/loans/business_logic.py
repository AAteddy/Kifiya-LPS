# loans/business_logic.py


import logging
from .models import LoanApplication, LoanRepayment
from django.utils import timezone

logger = logging.getLogger(__name__)


def validate_loan_application(loan_application):
    """Function to validate a loan application."""
    logger.debug("Validating loan application ID: %s", loan_application.id)
    errors = []
    borrower = loan_application.borrower
    if borrower.credit_score < 600:
        errors.append("Credit score too low")
    if borrower.annual_income <= 0:
        errors.append("Invalid annual income")
    if borrower.debt_to_income_ratio > 0.4:
        errors.append("Debt to income ratio too high")
    if errors:
        logger.warning(
            "Validation errors for loan application ID %s: %s",
            loan_application.id,
            errors,
        )
    else:
        logger.info(
            "Loan application ID %s validated successfully.", loan_application.id
        )
    return errors


def approve_loan(loan_application):
    """Function to approve a loan application."""
    logger.debug("Approving loan application ID: %s", loan_application.id)
    loan_application.status = "Approved"
    loan_application.approved_at = timezone.now()
    loan_application.save()
    logger.info("Loan application ID %s approved.", loan_application.id)


def disburse_loan(loan_application):
    """Function to disburse a loan."""
    logger.debug("Disbursing loan application ID: %s", loan_application.id)
    loan_application.status = "Disbursed"
    loan_application.disbursed_at = timezone.now()
    loan_application.save()
    logger.info("Loan application ID %s disbursed.", loan_application.id)


def record_repayment(loan_application, amount):
    """Function to record a loan repayment."""
    logger.debug("Recording repayment for loan application ID: %s", loan_application.id)
    LoanRepayment.objects.create(loan=loan_application, amount=amount)
    logger.info(
        "Repayment of amount %s recorded for loan application ID %s.",
        amount,
        loan_application.id,
    )
