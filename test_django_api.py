#!/usr/bin/env python3
"""
Test script for Django Credit Approval System API
Run this after starting the Django server to test all endpoints
"""

import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def test_api():
    print("🚀 Testing Django Credit Approval System API\n")
    
    # Test 1: Register Customer
    print("1. Testing Customer Registration...")
    customer_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 30,
        'monthly_income': 50000,
        'phone_number': 9876543210
    }
    
    try:
        response = requests.post(f'{BASE_URL}/register/', json=customer_data)
        if response.status_code == 201:
            customer = response.json()
            customer_id = customer['customer_id']
            print(f"✅ Customer registered successfully: {customer['name']} (ID: {customer_id})")
            print(f"   Approved Limit: ₹{customer['approved_limit']:,}")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    print()
    
    # Test 2: Check Eligibility
    print("2. Testing Loan Eligibility Check...")
    eligibility_data = {
        'customer_id': customer_id,
        'loan_amount': 100000,
        'interest_rate': 10.0,
        'tenure': 12
    }
    
    try:
        response = requests.post(f'{BASE_URL}/check-eligibility/', json=eligibility_data)
        if response.status_code == 200:
            eligibility = response.json()
            print(f"✅ Eligibility check completed:")
            print(f"   Approval: {eligibility['approval']}")
            print(f"   Interest Rate: {eligibility['interest_rate']}%")
            print(f"   Corrected Rate: {eligibility['corrected_interest_rate']}%")
            print(f"   Monthly EMI: ₹{eligibility['monthly_installment']}")
        else:
            print(f"❌ Eligibility check failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Eligibility check error: {e}")
    
    print()
    
    # Test 3: Create Loan
    print("3. Testing Loan Creation...")
    loan_data = {
        'customer_id': customer_id,
        'loan_amount': 100000,
        'interest_rate': 12.0,  # Use corrected rate
        'tenure': 12
    }
    
    try:
        response = requests.post(f'{BASE_URL}/create-loan/', json=loan_data)
        if response.status_code == 201:
            loan = response.json()
            loan_id = loan['loan_id']
            print(f"✅ Loan created successfully:")
            print(f"   Loan ID: {loan_id}")
            print(f"   Approved: {loan['loan_approved']}")
            print(f"   Monthly EMI: ₹{loan['monthly_installment']}")
            print(f"   Message: {loan['message']}")
        else:
            loan = response.json()
            print(f"⚠️ Loan creation response: {response.status_code}")
            print(f"   Approved: {loan.get('loan_approved', False)}")
            print(f"   Message: {loan.get('message', 'No message')}")
            loan_id = loan.get('loan_id')
    except Exception as e:
        print(f"❌ Loan creation error: {e}")
        loan_id = None
    
    print()
    
    # Test 4: View Loan Details (if loan was created)
    if loan_id:
        print("4. Testing View Loan Details...")
        try:
            response = requests.get(f'{BASE_URL}/view-loan/{loan_id}/')
            if response.status_code == 200:
                loan_details = response.json()
                print(f"✅ Loan details retrieved:")
                print(f"   Loan ID: {loan_details['loan_id']}")
                print(f"   Customer: {loan_details['customer']['name']}")
                print(f"   Amount: ₹{loan_details['loan_amount']}")
                print(f"   Interest Rate: {loan_details['interest_rate']}%")
                print(f"   Tenure: {loan_details['tenure']} months")
            else:
                print(f"❌ View loan failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ View loan error: {e}")
        
        print()
    
    # Test 5: View Customer Loans
    print("5. Testing View Customer Loans...")
    try:
        response = requests.get(f'{BASE_URL}/view-loans/{customer_id}/')
        if response.status_code == 200:
            customer_loans = response.json()
            print(f"✅ Customer loans retrieved: {len(customer_loans)} loan(s)")
            for loan in customer_loans:
                print(f"   Loan {loan['loan_id']}: ₹{loan['loan_amount']} at {loan['interest_rate']}%")
        else:
            print(f"❌ View customer loans failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ View customer loans error: {e}")
    
    print()
    
    # Test 6: Test with different credit scenarios
    print("6. Testing Different Credit Scenarios...")
    
    # Register another customer with higher income
    customer_data_2 = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'age': 35,
        'monthly_income': 100000,
        'phone_number': 9876543211
    }
    
    try:
        response = requests.post(f'{BASE_URL}/register/', json=customer_data_2)
        if response.status_code == 201:
            customer_2 = response.json()
            customer_id_2 = customer_2['customer_id']
            print(f"✅ Second customer registered: {customer_2['name']} (ID: {customer_id_2})")
            
            # Test high loan amount
            high_loan_data = {
                'customer_id': customer_id_2,
                'loan_amount': 500000,
                'interest_rate': 8.0,  # Low interest rate to test correction
                'tenure': 24
            }
            
            response = requests.post(f'{BASE_URL}/check-eligibility/', json=high_loan_data)
            if response.status_code == 200:
                eligibility = response.json()
                print(f"   High loan eligibility:")
                print(f"   Approval: {eligibility['approval']}")
                print(f"   Original Rate: {high_loan_data['interest_rate']}%")
                print(f"   Corrected Rate: {eligibility['corrected_interest_rate']}%")
        
    except Exception as e:
        print(f"❌ Second customer test error: {e}")
    
    print("\n🎉 API testing completed!")
    print("\n💡 Next steps:")
    print("1. Check Django admin at http://localhost:8000/admin/")
    print("2. Run unit tests: docker-compose exec web python manage.py test")
    print("3. Ingest sample data: docker-compose exec web python manage.py ingest_data")

if __name__ == '__main__':
    print("Waiting for Django server to start...")
    time.sleep(2)
    test_api()