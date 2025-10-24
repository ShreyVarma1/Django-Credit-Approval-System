from rest_framework import serializers
from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'name', 'age', 
                 'phone_number', 'monthly_salary', 'approved_limit']


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, source='monthly_salary')
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number']
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class CustomerResponseSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, source='monthly_salary')
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'age', 'monthly_income', 'approved_limit', 'phone_number']


class LoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class LoanCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanCreateResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2, source='monthly_repayment')
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 
                 'monthly_installment', 'tenure']


class CustomerLoanSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2, source='monthly_repayment')
    repayments_left = serializers.ReadOnlyField()
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'repayments_left']