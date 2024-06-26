from rest_framework import serializers
from .models import Borrower, LoanApplication, LoanRepayment


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = "__all__"


class LoanApplicationSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer()

    class Meta:
        model = LoanApplication
        fields = "__all__"


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ["amount", "date"]
        read_only_fields = ["date"]
