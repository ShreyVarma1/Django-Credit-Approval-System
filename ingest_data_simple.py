#!/usr/bin/env python
"""
Simple data ingestion script that runs without Celery
This directly processes the Excel files and imports data into Django models
"""

import os
import sys
import django
import pandas as pd
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_system.settings')
django.setup()

from loans.models import Customer, Loan

def ingest_customer_data():
    """Ingest customer data from customer_data.xlsx"""
    print("📊 Starting customer data ingestion...")
    
    try:
        # Read Excel file
        df = pd.read_excel('customer_data.xlsx')
        print(f"📋 Found {len(df)} customer records in Excel file")
        
        customers_created = 0
        customers_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Handle different possible column names
                customer_data = {
                    'first_name': str(row.get('first_name', row.get('First Name', ''))),
                    'last_name': str(row.get('last_name', row.get('Last Name', ''))),
                    'phone_number': int(row.get('phone_number', row.get('Phone Number', 0))),
                    'monthly_salary': Decimal(str(row.get('monthly_salary', row.get('Monthly Salary', 0)))),
                    'approved_limit': Decimal(str(row.get('approved_limit', row.get('Approved Limit', 0)))),
                    'current_debt': Decimal(str(row.get('current_debt', row.get('Current Debt', 0)))),
                }
                
                # Add age if available
                if 'age' in row or 'Age' in row:
                    customer_data['age'] = int(row.get('age', row.get('Age', 25)))
                else:
                    customer_data['age'] = 25  # Default age
                
                # Try to get existing customer by phone number
                customer, created = Customer.objects.get_or_create(
                    phone_number=customer_data['phone_number'],
                    defaults=customer_data
                )
                
                if created:
                    customers_created += 1
                    print(f"✅ Created customer: {customer.name}")
                else:
                    # Update existing customer
                    for key, value in customer_data.items():
                        setattr(customer, key, value)
                    customer.save()
                    customers_updated += 1
                    print(f"🔄 Updated customer: {customer.name}")
                    
            except Exception as e:
                error_msg = f"❌ Error processing customer row {index + 1}: {e}"
                print(error_msg)
                errors.append(error_msg)
                continue
        
        print(f"\n📊 Customer Data Ingestion Summary:")
        print(f"   ✅ Created: {customers_created}")
        print(f"   🔄 Updated: {customers_updated}")
        print(f"   ❌ Errors: {len(errors)}")
        
        return {
            'status': 'success',
            'created': customers_created,
            'updated': customers_updated,
            'errors': errors
        }
        
    except Exception as e:
        error_msg = f"❌ Error reading customer_data.xlsx: {e}"
        print(error_msg)
        return {'status': 'error', 'message': error_msg}

def ingest_loan_data():
    """Ingest loan data from loan_data.xlsx"""
    print("\n💰 Starting loan data ingestion...")
    
    try:
        # Read Excel file
        df = pd.read_excel('loan_data.xlsx')
        print(f"📋 Found {len(df)} loan records in Excel file")
        
        loans_created = 0
        loans_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Get customer ID
                customer_id = int(row.get('customer_id', row.get('Customer ID', 0)))
                
                # Get customer
                try:
                    customer = Customer.objects.get(customer_id=customer_id)
                except Customer.DoesNotExist:
                    error_msg = f"⚠️ Customer {customer_id} not found for loan in row {index + 1}"
                    print(error_msg)
                    errors.append(error_msg)
                    continue
                
                # Handle different possible column names
                loan_data = {
                    'customer': customer,
                    'loan_amount': Decimal(str(row.get('loan_amount', row.get('Loan Amount', 0)))),
                    'tenure': int(row.get('tenure', row.get('Tenure', 0))),
                    'interest_rate': Decimal(str(row.get('interest_rate', row.get('Interest Rate', 0)))),
                    'monthly_repayment': Decimal(str(row.get('monthly_repayment', row.get('Monthly Repayment', row.get('EMI', 0))))),
                    'emis_paid_on_time': int(row.get('emis_paid_on_time', row.get('EMIs Paid On Time', 0))),
                }
                
                # Handle dates
                try:
                    start_date = row.get('start_date', row.get('Start Date'))
                    end_date = row.get('end_date', row.get('End Date'))
                    
                    if pd.notna(start_date):
                        loan_data['start_date'] = pd.to_datetime(start_date).date()
                    else:
                        loan_data['start_date'] = pd.to_datetime('2023-01-01').date()
                        
                    if pd.notna(end_date):
                        loan_data['end_date'] = pd.to_datetime(end_date).date()
                    else:
                        # Calculate end date based on tenure
                        from datetime import timedelta
                        loan_data['end_date'] = loan_data['start_date'] + timedelta(days=loan_data['tenure'] * 30)
                        
                except Exception as date_error:
                    print(f"⚠️ Date parsing error for row {index + 1}: {date_error}")
                    loan_data['start_date'] = pd.to_datetime('2023-01-01').date()
                    loan_data['end_date'] = pd.to_datetime('2024-01-01').date()
                
                # Check if loan already exists
                existing_loan = Loan.objects.filter(
                    customer=customer,
                    loan_amount=loan_data['loan_amount'],
                    start_date=loan_data['start_date']
                ).first()
                
                if existing_loan:
                    # Update existing loan
                    for key, value in loan_data.items():
                        if key != 'customer':
                            setattr(existing_loan, key, value)
                    existing_loan.save()
                    loans_updated += 1
                    print(f"🔄 Updated loan for customer {customer.name}")
                else:
                    # Create new loan
                    loan = Loan.objects.create(**loan_data)
                    loans_created += 1
                    print(f"✅ Created loan {loan.loan_id} for customer {customer.name}")
                    
            except Exception as e:
                error_msg = f"❌ Error processing loan row {index + 1}: {e}"
                print(error_msg)
                errors.append(error_msg)
                continue
        
        print(f"\n💰 Loan Data Ingestion Summary:")
        print(f"   ✅ Created: {loans_created}")
        print(f"   🔄 Updated: {loans_updated}")
        print(f"   ❌ Errors: {len(errors)}")
        
        return {
            'status': 'success',
            'created': loans_created,
            'updated': loans_updated,
            'errors': errors
        }
        
    except Exception as e:
        error_msg = f"❌ Error reading loan_data.xlsx: {e}"
        print(error_msg)
        return {'status': 'error', 'message': error_msg}

def main():
    """Main function to run data ingestion"""
    print("🚀 Django Credit System - Data Ingestion")
    print("=" * 50)
    
    # Check if Excel files exist
    if not os.path.exists('customer_data.xlsx'):
        print("❌ customer_data.xlsx not found!")
        return
        
    if not os.path.exists('loan_data.xlsx'):
        print("❌ loan_data.xlsx not found!")
        return
    
    print("✅ Excel files found")
    
    # Run migrations first
    print("\n🗄️ Running database migrations...")
    os.system('python manage.py migrate')
    
    # Ingest customer data first
    customer_result = ingest_customer_data()
    
    # Then ingest loan data
    loan_result = ingest_loan_data()
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 Data Ingestion Completed!")
    print(f"📊 Customers: {customer_result.get('created', 0)} created, {customer_result.get('updated', 0)} updated")
    print(f"💰 Loans: {loan_result.get('created', 0)} created, {loan_result.get('updated', 0)} updated")
    
    if customer_result.get('errors') or loan_result.get('errors'):
        print(f"⚠️ Total errors: {len(customer_result.get('errors', [])) + len(loan_result.get('errors', []))}")
    
    print("\n💡 Next steps:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Test API: python test_django_api.py")
    print("3. Check admin: http://localhost:8000/admin/")

if __name__ == '__main__':
    main()