from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Customer, Loan
from .services import CreditScoreService, LoanEligibilityService


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        """Test customer creation with approved limit calculation"""
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=9876543210,
            monthly_salary=Decimal('50000')
        )
        
        # approved_limit = 36 * monthly_salary (rounded to nearest lakh)
        expected_limit = round(36 * 50000 / 100000) * 100000
        self.assertEqual(customer.approved_limit, expected_limit)
        self.assertEqual(customer.name, "John Doe")


class LoanModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=25,
            phone_number=9876543211,
            monthly_salary=Decimal('60000')
        )
    
    def test_loan_emi_calculation(self):
        """Test EMI calculation in loan model"""
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=Decimal('100000'),
            tenure=12,
            interest_rate=Decimal('12.0'),
            start_date='2024-01-01',
            end_date='2024-12-31'
        )
        
        # EMI should be calculated automatically
        self.assertGreater(loan.monthly_repayment, 0)


class CreditScoreServiceTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            age=35,
            phone_number=9876543212,
            monthly_salary=Decimal('75000')
        )
    
    def test_credit_score_new_customer(self):
        """Test credit score for new customer with no loans"""
        score = CreditScoreService.calculate_credit_score(self.customer.customer_id)
        self.assertEqual(score, 50)  # Default score for new customers
    
    def test_credit_score_with_loans(self):
        """Test credit score calculation with existing loans"""
        # Create a loan
        Loan.objects.create(
            customer=self.customer,
            loan_amount=Decimal('50000'),
            tenure=12,
            interest_rate=Decimal('10.0'),
            emis_paid_on_time=12,  # All EMIs paid on time
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        
        score = CreditScoreService.calculate_credit_score(self.customer.customer_id)
        self.assertGreater(score, 50)  # Should be higher than default


class APIEndpointsTest(APITestCase):
    def test_register_customer(self):
        """Test customer registration endpoint"""
        data = {
            'first_name': 'API',
            'last_name': 'Test',
            'age': 28,
            'monthly_income': 55000,
            'phone_number': 9876543213
        }
        
        response = self.client.post('/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('customer_id', response.data)
        self.assertEqual(response.data['name'], 'API Test')
    
    def test_check_eligibility(self):
        """Test loan eligibility check endpoint"""
        # First create a customer
        customer = Customer.objects.create(
            first_name="Eligibility",
            last_name="Test",
            age=30,
            phone_number=9876543214,
            monthly_salary=Decimal('80000')
        )
        
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 100000,
            'interest_rate': 10.0,
            'tenure': 24
        }
        
        response = self.client.post('/check-eligibility/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('approval', response.data)
        self.assertIn('monthly_installment', response.data)
    
    def test_create_loan(self):
        """Test loan creation endpoint"""
        # Create a customer with good credit profile
        customer = Customer.objects.create(
            first_name="Loan",
            last_name="Test",
            age=32,
            phone_number=9876543215,
            monthly_salary=Decimal('100000')
        )
        
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 200000,
            'interest_rate': 12.0,
            'tenure': 36
        }
        
        response = self.client.post('/create-loan/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['loan_approved'])
        self.assertIsNotNone(response.data['loan_id'])


class LoanEligibilityServiceTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Service",
            last_name="Test",
            age=29,
            phone_number=9876543216,
            monthly_salary=Decimal('70000')
        )
    
    def test_emi_calculation(self):
        """Test EMI calculation service"""
        emi = LoanEligibilityService.calculate_emi(
            principal=Decimal('100000'),
            annual_rate=Decimal('12.0'),
            tenure_months=12
        )
        
        self.assertGreater(emi, 0)
        self.assertIsInstance(emi, Decimal)
    
    def test_eligibility_high_credit_score(self):
        """Test eligibility for customer with high credit score"""
        # This would require mocking the credit score service
        # or creating a customer with good loan history
        pass