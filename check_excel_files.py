#!/usr/bin/env python
"""
Script to check the structure and content of Excel files
"""

import pandas as pd
import os

def check_excel_file(filename):
    """Check the structure of an Excel file"""
    print(f"\n📊 Checking {filename}...")
    print("=" * 50)
    
    if not os.path.exists(filename):
        print(f"❌ {filename} not found!")
        return
    
    try:
        # Read Excel file
        df = pd.read_excel(filename)
        
        print(f"✅ File loaded successfully")
        print(f"📋 Rows: {len(df)}")
        print(f"📋 Columns: {len(df.columns)}")
        
        print(f"\n📝 Column Names:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        print(f"\n📊 First 3 rows:")
        print(df.head(3).to_string())
        
        print(f"\n📈 Data Types:")
        print(df.dtypes.to_string())
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print(f"\n⚠️ Missing Values:")
            for col, count in missing.items():
                if count > 0:
                    print(f"   {col}: {count} missing")
        else:
            print(f"\n✅ No missing values found")
            
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")

def main():
    """Main function to check both Excel files"""
    print("🔍 Excel Files Structure Checker")
    print("=" * 50)
    
    # Check customer data
    check_excel_file('customer_data.xlsx')
    
    # Check loan data
    check_excel_file('loan_data.xlsx')
    
    print(f"\n💡 Tips:")
    print("1. Make sure column names match the expected format")
    print("2. Check for any missing or invalid data")
    print("3. Ensure date formats are consistent")
    print("4. Run 'python ingest_data_simple.py' to import the data")

if __name__ == '__main__':
    main()