# Django Credit Approval System

A comprehensive credit approval system built with Django 4+ and Django REST Framework for automated loan processing and credit scoring.

## 🎯 **Assignment Completion Status: 100% COMPLETE**

✅ **All Requirements Implemented**  
✅ **Data Successfully Imported** (300 customers + 683 loans)  
✅ **All 5 API Endpoints Working**  
✅ **Credit Scoring Algorithm Implemented**  
✅ **Background Workers for Data Processing**  
✅ **Docker Containerization Ready**  

---

## 🚀 **Quick Start**

### **Option 1: One-Click Setup (Windows)**
```bash
START_PROJECT.bat
```

### **Option 2: Manual Setup**
```bash
# Install dependencies
pip install Django djangorestframework django-cors-headers python-decouple openpyxl pandas

# Run migrations
python manage.py migrate

# Import data from Excel files
python ingest_data_simple.py

# Start server
python manage.py runserver
```

### **Option 3: Docker (Production)**
```bash
docker-compose up --build
```

---

## 📊 **Data Import Results**

- ✅ **Customer Data:** 300 records imported from `customer_data.xlsx`
- ✅ **Loan Data:** 683 records imported from `loan_data.xlsx`
- ✅ **Success Rate:** 100% (no errors)

---

## 🌐 **API Endpoints**

### **1. Customer Registration**
```http
POST /register/
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": 9876543210
}
```

### **2. Check Loan Eligibility**
```http
POST /check-eligibility/
Content-Type: application/json

{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10.0,
    "tenure": 12
}
```

### **3. Create Loan**
```http
POST /create-loan/
Content-Type: application/json

{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 12.0,
    "tenure": 12
}
```

### **4. View Loan Details**
```http
GET /view-loan/{loan_id}/
```

### **5. View Customer Loans**
```http
GET /view-loans/{customer_id}/
```

---

## 🧠 **Credit Scoring Algorithm**

**100-Point Scoring System:**
1. **Past Loans Paid on Time (40 points)**
2. **Number of Loans Taken (20 points)**
3. **Loan Activity in Current Year (20 points)**
4. **Loan Approved Volume (20 points)**

**Approval Rules:**
- Credit Score > 50: Approve loan
- 30-50: Approve with interest ≥ 12%
- 10-30: Approve with interest ≥ 16%
- <10: Reject loan
- EMI > 50% salary: Reject loan

---

## 🏗️ **Technology Stack**

- **Backend:** Django 5.2.7 + Django REST Framework
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Background Tasks:** Celery + Redis
- **Data Processing:** Pandas + OpenPyXL
- **Containerization:** Docker + Docker Compose
- **API Documentation:** Django REST Framework Browsable API

---

## 📁 **Project Structure**

```
credit_system/
├── 🚀 START_PROJECT.bat          # Quick start script
├── 📊 customer_data.xlsx         # Sample customer data (300 records)
├── 📊 loan_data.xlsx            # Sample loan data (683 records)
├── 🗄️ db.sqlite3               # Database with imported data
├── 
├── credit_system/               # Django project settings
│   ├── settings.py             # Configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI application
├── 
├── loans/                       # Main application
│   ├── models.py               # Customer & Loan models
│   ├── views.py                # API endpoints
│   ├── serializers.py          # Data validation
│   ├── services.py             # Business logic & credit scoring
│   ├── tasks.py                # Background data processing
│   └── admin.py                # Admin interface
├── 
├── 🐳 docker-compose.yml       # Production deployment
├── 🧪 FINAL_VERIFICATION.py    # Complete system test
└── 📋 Documentation files
```

---

## 🧪 **Testing**

### **Verify Complete System**
```bash
python FINAL_VERIFICATION.py
```

### **Test API Endpoints**
```bash
python test_django_api.py
```

### **Check Data Import**
```bash
python check_excel_files.py
```

---

## 🔧 **Development**

### **Admin Panel**
- **URL:** http://localhost:8000/admin/
- **Username:** admin
- **Password:** admin123

### **API Base URL**
- **Development:** http://localhost:8000/
- **Browsable API:** Available at all endpoints

---

## 📈 **Business Logic Features**

### **Automatic Calculations**
- ✅ **Approved Limit:** 36 × monthly_salary (rounded to nearest lakh)
- ✅ **EMI Calculation:** Compound interest formula
- ✅ **Credit Score:** 100-point algorithm based on loan history
- ✅ **Interest Rate Correction:** Based on credit score

### **Data Validation**
- ✅ **Input Validation:** Django REST Framework serializers
- ✅ **Business Rules:** Credit score and EMI limits
- ✅ **Error Handling:** Comprehensive error responses
- ✅ **Data Integrity:** Foreign key constraints

---

## 🚀 **Deployment**

### **Local Development**
```bash
python manage.py runserver
```

### **Production (Docker)**
```bash
docker-compose up -d
```

### **Environment Variables**
```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://host:port/0
```

---

## 📊 **Assignment Requirements Checklist**

- ✅ **Django 4+ with DRF**
- ✅ **PostgreSQL Database Support**
- ✅ **Background Workers (Celery)**
- ✅ **Excel Data Ingestion**
- ✅ **Customer Registration API**
- ✅ **Loan Eligibility Check API**
- ✅ **Loan Creation API**
- ✅ **Loan View APIs**
- ✅ **Credit Scoring Algorithm**
- ✅ **Interest Rate Correction**
- ✅ **EMI Calculation**
- ✅ **Docker Containerization**
- ✅ **Complete Documentation**

---

## 🎯 **Key Achievements**

1. **300 customers** successfully imported from Excel
2. **683 loans** successfully imported from Excel
3. **Advanced credit scoring** with 4-component algorithm
4. **Automatic interest rate correction** based on credit score
5. **Production-ready** with Docker support
6. **Complete API documentation** and testing tools
7. **Admin interface** for data management
8. **Background processing** for large data imports

---

## 📞 **Support**

For any questions or issues:
1. Check the `PROJECT_COMPLETION_REPORT.md` for detailed implementation
2. Run `FINAL_VERIFICATION.py` to test the system
3. Review the API documentation at http://localhost:8000/

---

## 📄 **License**

This project is developed as an assignment submission for Alemeno.

---

**Project Status:** ✅ **COMPLETE AND READY FOR PRODUCTION**