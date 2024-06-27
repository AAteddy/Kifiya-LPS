# loans/views.py


import logging
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

logger = logging.getLogger(__name__)


class LoanApplicationViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing loan applications.
    """

    def create(self, request):
        """
        Submit a new loan application.
        """
        logger.debug("Received request to create a loan application.")
        serializer = LoanApplicationSerializer(data=request.data)
        if serializer.is_valid():
            borrower_data = request.data.get("borrower")
            borrower_serializer = BorrowerSerializer(data=borrower_data)
            if borrower_serializer.is_valid():
                borrower = borrower_serializer.save()
                loan_application = serializer.save(borrower=borrower)
                validation_errors = validate_loan_application(loan_application)
                if validation_errors:
                    logger.warning("Validation errors: %s", validation_errors)
                    return Response(
                        validation_errors, status=status.HTTP_400_BAD_REQUEST
                    )
                logger.info("Loan application created successfully.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning("Borrower data invalid: %s", borrower_serializer.errors)
            return Response(
                borrower_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        logger.warning("Loan application data invalid: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve loan details by ID.
        """
        logger.debug("Received request to retrieve loan application with ID: %s", pk)
        try:
            loan = LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            logger.error("Loan application with ID %s does not exist.", pk)
            return Response(
                {"error": "Loan application with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError:
            logger.error("Invalid loan ID: %s. ID must be a number.", pk)
            return Response(
                {"error": "Invalid loan ID. ID must be a number."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = LoanApplicationSerializer(loan)
        logger.info("Retrieved loan application with ID: %s", pk)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def approve(self, request, pk=None):
        """
        Approve a loan application.
        """
        logger.debug("Received request to approve loan application with ID: %s", pk)
        try:
            loan = LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            logger.error("Loan application with ID %s does not exist.", pk)
            return Response(
                {"error": "Loan application with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if loan.status == "Approved":
            logger.warning("Loan application with ID %s is already approved.", pk)
            return Response(
                {"error": "loan already approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if loan.status != "Pending":
            logger.warning(
                "Loan application with ID %s cannot be approved as it is not in 'Pending' status.",
                pk,
            )
            return Response(
                {"error": "Loan cannot be approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validation_errors = validate_loan_application(loan)
        if validation_errors:
            logger.warning(
                "Validation errors for loan application ID %s: %s",
                pk,
                validation_errors,
            )
            return Response(
                {"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST
            )

        approve_loan(loan)
        logger.info("Loan application with ID %s approved.", pk)
        return Response({"status": "Loan approved"})

    @action(detail=True, methods=["put"])
    def reject(self, request, pk=None):
        """
        Reject a loan application.
        """
        logger.debug("Received request to reject loan application with ID: %s", pk)
        try:
            loan = LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            logger.error("Loan application with ID %s does not exist.", pk)
            return Response(
                {"error": "Loan application with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if loan.status == "Rejected":
            logger.warning("Loan application with ID %s is already rejected.", pk)
            return Response(
                {"error": "loan already rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if loan.status != "Pending":
            logger.warning(
                "Loan application with ID %s cannot be rejected as it is not in 'Pending' status.",
                pk,
            )
            return Response(
                {"error": "Loan cannot be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan.status = "Rejected"
        loan.save()
        logger.info("Loan application with ID %s rejected.", pk)
        return Response({"status": "Loan rejected"})

    @action(detail=True, methods=["post"])
    def disburse(self, request, pk=None):
        """
        Disburse an approved loan.
        """
        logger.debug("Received request to disburse loan application with ID: %s", pk)
        try:
            loan = LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            logger.error("Loan application with ID %s does not exist.", pk)
            return Response(
                {"error": "Loan application with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if loan.status != "Approved":
            logger.warning(
                "Loan application with ID %s cannot be disbursed as it is not in 'Approved' status.",
                pk,
            )
            return Response(
                {"error": "Loan cannot be disbursed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        disburse_loan(loan)
        logger.info("Loan application with ID %s disbursed.", pk)
        return Response({"status": "Loan disbursed"})

    @action(detail=True, methods=["post"])
    def repay(self, request, pk=None):
        """
        Record a loan repayment.
        """
        logger.debug("Received request to record repayment for loan ID: %s", pk)
        try:
            loan = LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            logger.error("Loan application with ID %s does not exist.", pk)
            return Response(
                {"error": "Loan application with the specified ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if loan.status != "Disbursed":
            logger.warning(
                "Loan application with ID %s cannot be repaid as it is not in 'Disbursed' status.",
                pk,
            )
            return Response(
                {"error": "Loan cannot be repaid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = LoanRepaymentSerializer(data=request.data)
        if serializer.is_valid():
            record_repayment(loan, serializer.validated_data["amount"])
            logger.info("Repayment recorded for loan ID: %s", pk)
            return Response({"status": "Repayment recorded"})
        logger.warning("Repayment data invalid: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
