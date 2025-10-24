@echo off
echo Setting up Git repository for Django Credit Approval System...
echo.

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Creating initial commit...
git commit -m "Complete Django Credit Approval System implementation"

echo.
echo Git repository setup complete!
echo.
echo Next steps:
echo 1. Create repository on GitHub: django-credit-approval-system
echo 2. Run: git remote add origin https://github.com/[YOUR_USERNAME]/django-credit-approval-system.git
echo 3. Run: git push -u origin main
echo.
echo Replace [YOUR_USERNAME] with your actual GitHub username
pause