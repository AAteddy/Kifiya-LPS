from django.db import models
from django.utils import timezone


class Borrower(models.Model):
    """Borrower model that defines the
    borrower.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    credit_score = models.IntegerField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    debt_to_income_ratio = models.DecimalField(max_digits=5, decimal_places=2)


class LoanApplication(models.Model):
    """LoanApplication model that defines the
    loan application.
    """

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.FloatField()
    term = models.IntegerField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)


class LoanRepayment(models.Model):
    """LoanRepayment model that defines the
    loan repayment.
    """

    # loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan = models.ForeignKey(
        LoanApplication, related_name="repayments", on_delete=models.CASCADE
    )
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
