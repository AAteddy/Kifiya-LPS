from rest_framework import serializers
from .models import Borrower, LoanApplication, LoanRepayment


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = "__all__"
