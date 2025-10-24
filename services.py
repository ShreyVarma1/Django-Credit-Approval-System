from decimal import Decimal
from datetime import datetime, date
from django.db.models import Sum, Count, Q, F
from .models import Customer, Loan


class CreditScoreService:
    """Service to calculate credit score based on historical data"""
    
    @staticmethod
    def calculate_credit_score(customer_id):
        """
        Calculate credit score out of 100 based on:
        i. Past Loans paid on time
        ii. No of loans taken in past
        iii. Loan activity in current year
        iv. Loan approved volume
        v. If sum of current loans > approved limit, credit score = 0
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return 0
        
        loans = Loan.objects.filter(customer=customer)
        
        if not loans.exists():
            return 50  # Default score for new customers
        
        # Check if current loans exceed approved limit
        current_loans_sum = loans.aggregate(
            total=Sum('loan_amount')
        )['total'] or Decimal('0')
        
        if current_loans_sum > customer.approved_limit:
            return 0
        
        # Component 1: Past Loans paid on time (40 points)
        total_loans = loans.count()
        loans_paid_on_time = loans.filter(
            emis_paid_on_time__gte=F('tenure')
        ).count()
        
        if total_loans > 0:
            on_time_score = (loans_paid_on_time / total_loans) * 40
        else:
            on_time_score = 20  # Default for new customers
        
        # Component 2: Number of loans taken (20 points - fewer loans = better score)
        if total_loans <= 2:
            loan_count_score = 20
        elif total_loans <= 5:
            loan_count_score = 15
        elif total_loans <= 10:
            loan_count_score = 10
        else:
            loan_count_score = 5
        
        # Component 3: Loan activity in current year (20 points)
        current_year = datetime.now().year
        current_year_loans = loans.filter(start_date__year=current_year).count()
        
        if current_year_loans == 0:
            current_year_score = 20
        elif current_year_loans <= 2:
            current_year_score = 15
        elif current_year_loans <= 4:
            current_year_score = 10
        else:
            current_year_score = 5
        
        # Component 4: Loan approved volume (20 points)
        total_approved_volume = loans.aggregate(
            total=Sum('loan_amount')
        )['total'] or Decimal('0')
        
        volume_ratio = float(total_approved_volume) / float(customer.approved_limit)
        
        if volume_ratio <= 0.3:
            volume_score = 20
        elif volume_ratio <= 0.6:
            volume_score = 15
        elif volume_ratio <= 0.8:
            volume_score = 10
        else:
            volume_score = 5
        
        total_score = on_time_score + loan_count_score + current_year_score + volume_score
        return min(100, max(0, int(total_score)))


class LoanEligibilityService:
    """Service to check loan eligibility and determine interest rates"""
    
    @staticmethod
    def check_eligibility(customer_id, loan_amount, interest_rate, tenure):
        """Check loan eligibility based on credit score and other criteria"""
        
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return {
                'approval': False,
                'message': 'Customer not found',
                'corrected_interest_rate': interest_rate,
                'monthly_installment': 0
            }
        
        # Calculate credit score
        credit_score = CreditScoreService.calculate_credit_score(customer_id)
        
        # Check if sum of all current EMIs > 50% of monthly salary
        current_emis = Loan.objects.filter(
            customer=customer,
            end_date__gte=date.today()
        ).aggregate(
            total_emi=Sum('monthly_repayment')
        )['total_emi'] or Decimal('0')
        
        max_allowed_emi = customer.monthly_salary * Decimal('0.5')
        
        # Calculate proposed EMI
        monthly_installment = LoanEligibilityService.calculate_emi(
            loan_amount, interest_rate, tenure
        )
        
        if current_emis + monthly_installment > max_allowed_emi:
            return {
                'approval': False,
                'message': 'EMI exceeds 50% of monthly salary',
                'corrected_interest_rate': interest_rate,
                'monthly_installment': monthly_installment
            }
        
        # Determine approval and corrected interest rate based on credit score
        if credit_score > 50:
            approval = True
            corrected_interest_rate = interest_rate
            message = 'Loan approved'
        elif 30 < credit_score <= 50:
            if interest_rate >= 12:
                approval = True
                corrected_interest_rate = interest_rate
                message = 'Loan approved'
            else:
                approval = True
                corrected_interest_rate = Decimal('12.0')
                message = 'Loan approved with corrected interest rate'
        elif 10 < credit_score <= 30:
            if interest_rate >= 16:
                approval = True
                corrected_interest_rate = interest_rate
                message = 'Loan approved'
            else:
                approval = True
                corrected_interest_rate = Decimal('16.0')
                message = 'Loan approved with corrected interest rate'
        else:  # credit_score <= 10
            approval = False
            corrected_interest_rate = interest_rate
            message = 'Loan not approved due to low credit score'
        
        # Recalculate EMI with corrected interest rate
        if approval and corrected_interest_rate != interest_rate:
            monthly_installment = LoanEligibilityService.calculate_emi(
                loan_amount, corrected_interest_rate, tenure
            )
        
        return {
            'approval': approval,
            'message': message,
            'corrected_interest_rate': corrected_interest_rate,
            'monthly_installment': monthly_installment,
            'credit_score': credit_score  # For debugging
        }
    
    @staticmethod
    def calculate_emi(principal, annual_rate, tenure_months):
        """Calculate EMI using compound interest formula"""
        principal = float(principal)
        monthly_rate = float(annual_rate) / (12 * 100)
        n = int(tenure_months)
        
        if monthly_rate == 0:
            return Decimal(str(principal / n))
        
        emi = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
        return Decimal(str(round(emi, 2)))