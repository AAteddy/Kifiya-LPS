# loans/test_business_logic.py

from django.test import TestCase
from django.utils import timezone
from .models import Borrower, LoanApplication, LoanRepayment
from .business_logic import (
    validate_loan_application,
    approve_loan,
    disburse_loan,
    record_repayment,
)


class BusinessLogicTests(TestCase):
    """Unittest for the business_logic"""

    def setUp(self):
        self.borrower = Borrower.objects.create(
            name="John Doe",
            credit_score=650,
            annual_income=50000,
            debt_to_income_ratio=0.2,
        )
        self.loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=self.borrower, status="Pending"
        )

    def test_validate_loan_application(self):
        """Test case for validating a loan application"""

        errors = validate_loan_application(self.loan)
        self.assertEqual(errors, [])

        self.borrower.credit_score = 550
        self.borrower.save()
        errors = validate_loan_application(self.loan)
        self.assertIn("Credit score too low", errors)

    def test_approve_loan(self):
        """Test case for validating a loan application approval"""

        approve_loan(self.loan)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, "Approved")
        self.assertIsNotNone(self.loan.approved_at)

    def test_disburse_loan(self):
        """Test case for validating a loan application disburse"""

        self.loan.status = "Approved"
        self.loan.save()
        disburse_loan(self.loan)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, "Disbursed")
        self.assertIsNotNone(self.loan.disbursed_at)

    def test_record_repayment(self):
        """Test case for validating a loan application repayment"""

        self.loan.status = "Disbursed"
        self.loan.save()
        record_repayment(self.loan, 500)
        self.assertEqual(LoanRepayment.objects.count(), 1)
        repayment = LoanRepayment.objects.first()
        self.assertEqual(repayment.amount, 500)
        self.assertEqual(repayment.loan, self.loan)
