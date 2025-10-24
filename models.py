from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import math


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    phone_number = models.BigIntegerField()
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=12, decimal_places=2)
    current_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
    
    def save(self, *args, **kwargs):
        if not self.approved_limit:
            # approved_limit = 36 * monthly_salary (rounded to nearest lakh)
            limit = 36 * self.monthly_salary
            self.approved_limit = round(limit / 100000) * 100000
        super().save(*args, **kwargs)
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.name} (ID: {self.customer_id})"


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=12, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
    
    def save(self, *args, **kwargs):
        if not self.monthly_repayment:
            # Calculate EMI using compound interest formula
            # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
            principal = float(self.loan_amount)
            monthly_rate = float(self.interest_rate) / (12 * 100)
            n = self.tenure
            
            if monthly_rate == 0:
                self.monthly_repayment = principal / n
            else:
                emi = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
                self.monthly_repayment = round(emi, 2)
        
        super().save(*args, **kwargs)
    
    @property
    def repayments_left(self):
        return self.tenure - self.emis_paid_on_time
    
    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer.name}"