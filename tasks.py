from celery import shared_task
import pandas as pd
from decimal import Decimal
from datetime import datetime
from .models import Customer, Loan
import logging

logger = logging.getLogger(__name__)


@shared_task
def ingest_customer_data(file_path):
    """
    Background task to ingest customer data from Excel file
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        customers_created = 0
        customers_updated = 0
        
        for _, row in df.iterrows():
            try:
                customer_data = {
                    'first_name': row.get('first_name', ''),
                    'last_name': row.get('last_name', ''),
                    'phone_number': int(row.get('phone_number', 0)),
                    'monthly_salary': Decimal(str(row.get('monthly_salary', 0))),
                    'approved_limit': Decimal(str(row.get('approved_limit', 0))),
                    'current_debt': Decimal(str(row.get('current_debt', 0))),
                }
                
                # Try to get existing customer by phone number
                customer, created = Customer.objects.get_or_create(
                    phone_number=customer_data['phone_number'],
                    defaults=customer_data
                )
                
                if created:
                    customers_created += 1
                    logger.info(f"Created customer: {customer.name}")
                else:
                    # Update existing customer
                    for key, value in customer_data.items():
                        setattr(customer, key, value)
                    customer.save()
                    customers_updated += 1
                    logger.info(f"Updated customer: {customer.name}")
                    
            except Exception as e:
                logger.error(f"Error processing customer row: {e}")
                continue
        
        logger.info(f"Customer data ingestion completed. Created: {customers_created}, Updated: {customers_updated}")
        return {
            'status': 'success',
            'customers_created': customers_created,
            'customers_updated': customers_updated
        }
        
    except Exception as e:
        logger.error(f"Error in customer data ingestion: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def ingest_loan_data(file_path):
    """
    Background task to ingest loan data from Excel file
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        loans_created = 0
        loans_updated = 0
        
        for _, row in df.iterrows():
            try:
                customer_id = int(row.get('customer_id', 0))
                
                # Get customer
                try:
                    customer = Customer.objects.get(customer_id=customer_id)
                except Customer.DoesNotExist:
                    logger.warning(f"Customer {customer_id} not found for loan")
                    continue
                
                loan_data = {
                    'customer': customer,
                    'loan_amount': Decimal(str(row.get('loan_amount', 0))),
                    'tenure': int(row.get('tenure', 0)),
                    'interest_rate': Decimal(str(row.get('interest_rate', 0))),
                    'monthly_repayment': Decimal(str(row.get('monthly_repayment', 0))),
                    'emis_paid_on_time': int(row.get('emis_paid_on_time', 0)),
                    'start_date': pd.to_datetime(row.get('start_date')).date(),
                    'end_date': pd.to_datetime(row.get('end_date')).date(),
                }
                
                # Check if loan already exists (by customer and loan amount and start date)
                existing_loan = Loan.objects.filter(
                    customer=customer,
                    loan_amount=loan_data['loan_amount'],
                    start_date=loan_data['start_date']
                ).first()
                
                if existing_loan:
                    # Update existing loan
                    for key, value in loan_data.items():
                        if key != 'customer':  # Don't update customer reference
                            setattr(existing_loan, key, value)
                    existing_loan.save()
                    loans_updated += 1
                    logger.info(f"Updated loan for customer {customer.name}")
                else:
                    # Create new loan
                    loan = Loan.objects.create(**loan_data)
                    loans_created += 1
                    logger.info(f"Created loan {loan.loan_id} for customer {customer.name}")
                    
            except Exception as e:
                logger.error(f"Error processing loan row: {e}")
                continue
        
        logger.info(f"Loan data ingestion completed. Created: {loans_created}, Updated: {loans_updated}")
        return {
            'status': 'success',
            'loans_created': loans_created,
            'loans_updated': loans_updated
        }
        
    except Exception as e:
        logger.error(f"Error in loan data ingestion: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def ingest_all_data():
    """
    Task to ingest both customer and loan data
    """
    try:
        # Ingest customer data first
        customer_result = ingest_customer_data('customer_data.xlsx')
        
        # Then ingest loan data
        loan_result = ingest_loan_data('loan_data.xlsx')
        
        return {
            'status': 'success',
            'customer_result': customer_result,
            'loan_result': loan_result
        }
        
    except Exception as e:
        logger.error(f"Error in data ingestion: {e}")
        return {'status': 'error', 'message': str(e)}