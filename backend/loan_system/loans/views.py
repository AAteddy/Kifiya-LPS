from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Borrower, LoanApplication, LoanRepayment
from .serializers import (
    BorrowerSerializer,
    LoanApplicationSerializer,
    LoanRepaymentSerializer,
)
from .business_logic import (
    validate_loan_application,
    approve_loan,
    disburse_loan,
    record_repayment,
)


class LoanApplicationViewSet(viewsets.ViewSet):
    def create(self, request):
        """Handles the creation of a new loan application."""
        serializer = LoanApplicationSerializer(data=request.data)
        if serializer.is_valid():
            borrower_data = request.data.get("borrower")
            borrower_serializer = BorrowerSerializer(data=borrower_data)
            if borrower_serializer.is_valid():
                borrower = borrower_serializer.save()
                serializer.save(borrower=borrower)
                validation_errors = validate_loan_application(serializer.instance)
                if validation_errors:
                    return Response(
                        validation_errors, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                borrower_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles retrieving a loan application by ID."""
        try:
            loan = LoanApplication.objects.get(pk=pk)
            serializer = LoanApplicationSerializer(loan)
            return Response(serializer.data)
        except LoanApplication.DoesNotExist:
            return Response(
                {"error": "LoanApplication with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["put"])
    def approve(self, request, pk=None):
        """Handles action for approving a loan."""
        loan = get_object_or_404(LoanApplication, pk=pk)
        if loan.status != "Pending":
            return Response(
                {"error": "Loan cannot be approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        approve_loan(loan)
        return Response({"status": "Loan approved"})

    @action(detail=True, methods=["put"])
    def reject(self, request, pk=None):
        """Handles action for rejecting a loan."""
        loan = get_object_or_404(LoanApplication, pk=pk)
        if loan.status != "Pending":
            return Response(
                {"error": "Loan cannot be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan.status = "Rejected"
        loan.save()
        return Response({"status": "Loan rejected"})

    @action(detail=True, methods=["post"])
    def disburse(self, request, pk=None):
        """Handles action for disbursement of loan."""
        loan = get_object_or_404(LoanApplication, pk=pk)
        if loan.status != "Approved":
            return Response(
                {"error": "Loan cannot be disbursed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        disburse_loan(loan)
        return Response({"status": "Loan disbursed"})

    @action(detail=True, methods=["post"])
    def repay(self, request, pk=None):
        """Handles action for recording a loan repayment."""
        loan = get_object_or_404(LoanApplication, pk=pk)
        serializer = LoanRepaymentSerializer(data=request.data)
        if serializer.is_valid():
            LoanRepayment.objects.create(
                loan=loan, amount=serializer.validated_data["amount"]
            )
            return Response({"status": "Repayment recorded"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
