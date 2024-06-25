from django.db import models
from django.utils import timezone


class Borrower(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    credit_score = models.IntegerField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    debt_to_income_ratio = models.DecimalField(max_digits=5, decimal_places=2)


class LoanApplication(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)
