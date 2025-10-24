# Credit Approval System - Django Backend

A comprehensive credit approval system built with Django 4+ and Django REST Framework, featuring automated credit scoring, loan eligibility assessment, and background data processing.

## 🚀 Features

- **Customer Management**: Registration with automatic credit limit calculation
- **Credit Scoring**: Intelligent scoring based on historical loan data
- **Loan Eligibility**: Real-time eligibility assessment with interest rate correction
- **Loan Processing**: Complete loan lifecycle management
- **Background Tasks**: Asynchronous data ingestion using Celery
- **Dockerized**: Complete containerization with Docker Compose

## 🛠 Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL 15
- **Task Queue**: Celery with Redis
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas for Excel file handling

## 📋 API Endpoints

### 1. Customer Registration
```
POST /register/
```
**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": 9876543210
}
```

**Response:**
```json
{
    "customer_id": 1,
    "name": "John Doe",
    "age": 30,
    "monthly_income": 50000,
    "approved_limit": 1800000,
    "phone_number": 9876543210
}
```

### 2. Check Loan Eligibility
```
POST /check-eligibility/
```
**Request Body:**
```json
{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10.0,
    "tenure": 12
}
```

**Response:**
```json
{
    "customer_id": 1,
    "approval": true,
    "interest_rate": 10.0,
    "corrected_interest_rate": 12.0,
    "tenure": 12,
    "monthly_installment": 8884.88
}
```

### 3. Create Loan
```
POST /create-loan/
```
**Request Body:**
```json
{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 12.0,
    "tenure": 12
}
```

**Response:**
```json
{
    "loan_id": 1,
    "customer_id": 1,
    "loan_approved": true,
    "message": "Loan approved and created successfully",
    "monthly_installment": 8884.88
}
```

### 4. View Loan Details
```
GET /view-loan/{loan_id}/
```

### 5. View Customer Loans
```
GET /view-loans/{customer_id}/
```

## 🏗 Project Structure

```
credit_system/
├── credit_system/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── loans/                  # Main application
│   ├── models.py          # Customer and Loan models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── services.py        # Business logic services
│   ├── tasks.py           # Celery background tasks
│   ├── urls.py            # URL routing
│   ├── admin.py           # Django admin
│   ├── tests.py           # Unit tests
│   └── management/        # Custom management commands
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Multi-container setup
└── README_DJANGO.md       # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd credit_system
cp .env.example .env
```

### 2. Build and Run with Docker
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Initialize Database
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser

# Ingest sample data
docker-compose exec web python manage.py ingest_data
```

### 4. Access the Application
- **API Base URL**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Database**: PostgreSQL on localhost:5432
- **Redis**: Redis on localhost:6379

## 📊 Credit Scoring Algorithm

The system calculates credit scores (0-100) based on:

1. **Past Loans Paid on Time (40 points)**
   - Percentage of loans with all EMIs paid on time

2. **Number of Loans Taken (20 points)**
   - Fewer loans = higher score
   - ≤2 loans: 20 points
   - 3-5 loans: 15 points
   - 6-10 loans: 10 points
   - >10 loans: 5 points

3. **Loan Activity in Current Year (20 points)**
   - Recent loan activity affects score
   - 0 loans: 20 points
   - 1-2 loans: 15 points
   - 3-4 loans: 10 points
   - >4 loans: 5 points

4. **Loan Approved Volume (20 points)**
   - Based on ratio of total loans to approved limit
   - ≤30%: 20 points
   - 31-60%: 15 points
   - 61-80%: 10 points
   - >80%: 5 points

### Approval Rules
- **Credit Score > 50**: Approve loan
- **30 < Credit Score ≤ 50**: Approve with interest rate ≥ 12%
- **10 < Credit Score ≤ 30**: Approve with interest rate ≥ 16%
- **Credit Score ≤ 10**: Reject loan
- **Current EMIs > 50% of salary**: Reject loan

## 🔧 Development

### Local Development (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL and Redis locally
# Update DATABASE_URL and REDIS_URL in .env

# Run migrations
python manage.py migrate

# Start Celery worker (separate terminal)
celery -A credit_system worker --loglevel=info

# Start Django server
python manage.py runserver
```

### Running Tests
```bash
# With Docker
docker-compose exec web python manage.py test

# Local
python manage.py test
```

### Data Ingestion
The system supports background ingestion of Excel files:

1. Place `customer_data.xlsx` and `loan_data.xlsx` in the project root
2. Run: `docker-compose exec web python manage.py ingest_data`

## 📁 Sample Data Format

### customer_data.xlsx
| customer_id | first_name | last_name | phone_number | monthly_salary | approved_limit | current_debt |
|-------------|------------|-----------|--------------|----------------|----------------|--------------|
| 1           | John       | Doe       | 9876543210   | 50000          | 1800000        | 0            |

### loan_data.xlsx
| customer_id | loan_id | loan_amount | tenure | interest_rate | monthly_repayment | emis_paid_on_time | start_date | end_date   |
|-------------|---------|-------------|--------|---------------|-------------------|-------------------|------------|------------|
| 1           | 1       | 100000      | 12     | 12.0          | 8884.88           | 12                | 2023-01-01 | 2023-12-31 |

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart services
   docker-compose restart
   ```

2. **Celery Tasks Not Running**
   ```bash
   # Check Celery worker logs
   docker-compose logs celery
   
   # Restart Celery
   docker-compose restart celery
   ```

3. **Port Already in Use**
   ```bash
   # Change ports in docker-compose.yml
   # Or stop conflicting services
   sudo lsof -i :8000
   ```

## 🔒 Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Implement proper authentication for production use
- Add rate limiting for API endpoints

## 📈 Performance Optimization

- Database indexes on frequently queried fields
- Celery for background processing
- Redis for caching (can be extended)
- Pagination for large datasets
- Connection pooling for database

## 🚀 Deployment

### Production Deployment
1. Set environment variables properly
2. Use a production WSGI server (Gunicorn included)
3. Set up reverse proxy (Nginx)
4. Configure SSL/TLS
5. Set up monitoring and logging
6. Use managed database services

### Environment Variables
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://host:port/0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 📝 API Documentation

For detailed API documentation, you can:
1. Use Django REST Framework's browsable API at http://localhost:8000/
2. Add django-rest-swagger for Swagger documentation
3. Use tools like Postman with the provided endpoint examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.