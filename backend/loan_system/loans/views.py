from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
