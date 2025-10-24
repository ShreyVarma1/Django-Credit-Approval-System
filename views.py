from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer, CustomerResponseSerializer,
    LoanEligibilitySerializer, LoanEligibilityResponseSerializer,
    LoanCreateSerializer, LoanCreateResponseSerializer,
    LoanDetailSerializer, CustomerLoanSerializer
)
from .services import LoanEligibilityService


@api_view(['POST'])
def register_customer(request):
    """
    Register a new customer with approved limit based on salary
    """
    serializer = CustomerRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerResponseSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """
    Check loan eligibility based on credit score and other criteria
    """
    serializer = LoanEligibilitySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Check eligibility using service
    eligibility_result = LoanEligibilityService.check_eligibility(
        customer_id=data['customer_id'],
        loan_amount=data['loan_amount'],
        interest_rate=data['interest_rate'],
        tenure=data['tenure']
    )
    
    response_data = {
        'customer_id': data['customer_id'],
        'approval': eligibility_result['approval'],
        'interest_rate': data['interest_rate'],
        'corrected_interest_rate': eligibility_result['corrected_interest_rate'],
        'tenure': data['tenure'],
        'monthly_installment': eligibility_result['monthly_installment']
    }
    
    response_serializer = LoanEligibilityResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_loan(request):
    """
    Process a new loan based on eligibility
    """
    serializer = LoanCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Check eligibility first
    eligibility_result = LoanEligibilityService.check_eligibility(
        customer_id=data['customer_id'],
        loan_amount=data['loan_amount'],
        interest_rate=data['interest_rate'],
        tenure=data['tenure']
    )
    
    if not eligibility_result['approval']:
        response_data = {
            'loan_id': None,
            'customer_id': data['customer_id'],
            'loan_approved': False,
            'message': eligibility_result['message'],
            'monthly_installment': eligibility_result['monthly_installment']
        }
        response_serializer = LoanCreateResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    # Create the loan
    try:
        customer = Customer.objects.get(customer_id=data['customer_id'])
        
        # Use corrected interest rate
        final_interest_rate = eligibility_result['corrected_interest_rate']
        
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data['loan_amount'],
            tenure=data['tenure'],
            interest_rate=final_interest_rate,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=data['tenure'] * 30)  # Approximate
        )
        
        response_data = {
            'loan_id': loan.loan_id,
            'customer_id': data['customer_id'],
            'loan_approved': True,
            'message': 'Loan approved and created successfully',
            'monthly_installment': loan.monthly_repayment
        }
        
        response_serializer = LoanCreateResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
    except Customer.DoesNotExist:
        response_data = {
            'loan_id': None,
            'customer_id': data['customer_id'],
            'loan_approved': False,
            'message': 'Customer not found',
            'monthly_installment': 0
        }
        response_serializer = LoanCreateResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_loan(request, loan_id):
    """
    View loan details and customer details
    """
    try:
        loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Loan not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def view_customer_loans(request, customer_id):
    """
    View all current loan details by customer id
    """
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        serializer = CustomerLoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )