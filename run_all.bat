@echo off
echo 🚀 Starting Indian Stock Analyzer with Telegram Bot...

:: Navigate to the project root
cd /d "c:\Users\user\OneDrive\Documents\stock\stock\indian-stock-analyzer"

:: Start Backend in a new window
echo 📡 Starting Backend...
start cmd /k "python backend\main.py"

:: Start Frontend in a new window
echo 🎨 Starting Frontend...
cd frontend
start cmd /k "npm run dev"

echo ✨ All systems are starting! 
echo Check the new terminal windows for logs and Telegram bot status.
pause
