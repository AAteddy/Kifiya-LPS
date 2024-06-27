# loans/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Borrower, LoanApplication


class LoanApplicationViewSetTests(APITestCase):
    """Unittest for the loan application"""

    def setUp(self):
        self.client = APIClient()
        self.borrower_data = {
            "name": "John Doe",
            "email": "johnnasondoe@example.com",
            "credit_score": 650,
            "annual_income": 50000,
            "debt_to_income_ratio": 0.2,
        }
        self.loan_application_data = {
            "amount": 10000,
            "term": 12,
            "purpose": "House Morgage",
            "borrower": self.borrower_data,
        }

    def test_create_loan_application(self):
        """Test case for creating a loan application"""

        url = reverse("loanapplication-list")  # Assuming you have a router registered
        response = self.client.post(url, self.loan_application_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanApplication.objects.count(), 1)
        self.assertEqual(Borrower.objects.count(), 1)

    def test_retrieve_loan_application(self):
        """Test case for retrieving a loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(amount=10000, term=12, borrower=borrower)
        url = reverse("loanapplication-detail", args=[loan.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 10000)

    def test_approve_loan_application(self):
        """Test case for approving a loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=borrower, status="Pending"
        )
        url = reverse("loanapplication-approve", args=[loan.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "Approved")

    def test_approve_already_approved_loan(self):
        """Test case for approving an already approved loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=borrower, status="Approved"
        )
        url = reverse("loanapplication-approve", args=[loan.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "loan already approved")

    def test_reject_loan_application(self):
        """Test case for rejecting a loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=borrower, status="Pending"
        )
        url = reverse("loanapplication-reject", args=[loan.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "Rejected")

    def test_disburse_loan_application(self):
        """Test case for disbursing an approved loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=borrower, status="Approved"
        )
        url = reverse("loanapplication-disburse", args=[loan.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "Disbursed")

    def test_repay_loan_application(self):
        """Test case for repaying a loan application"""

        borrower = Borrower.objects.create(**self.borrower_data)
        loan = LoanApplication.objects.create(
            amount=10000, term=12, borrower=borrower, status="Disbursed"
        )
        repayment_data = {"amount": 500}
        url = reverse("loanapplication-repay", args=[loan.pk])
        response = self.client.post(url, repayment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(loan.repayments.count(), 1)
        self.assertEqual(loan.repayments.first().amount, 500)
