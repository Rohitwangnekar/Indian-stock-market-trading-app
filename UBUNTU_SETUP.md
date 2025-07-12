# 🐧 Ubuntu Setup Guide - Indian Stock Market Trading App

This guide will help you set up and run the Indian Stock Market Trading App on Ubuntu Linux.

## 📋 Prerequisites

### System Requirements
- Ubuntu 18.04 LTS or later
- At least 2GB RAM
- 1GB free disk space
- Internet connection

### Required Software
- Python 3.8 or later
- Git
- pip (Python package manager)

## 🚀 Step-by-Step Installation

### 1. Update Your System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Python and Dependencies
```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv python3-dev -y

# Install Git
sudo apt install git -y

# Install build essentials (required for some Python packages)
sudo apt install build-essential libssl-dev libffi-dev -y

# Install PostgreSQL dependencies (optional, for production)
sudo apt install postgresql postgresql-contrib libpq-dev -y
```

### 3. Verify Installation
```bash
python3 --version  # Should show Python 3.8+
pip3 --version     # Should show pip version
git --version      # Should show Git version
```

### 4. Clone the Repository
```bash
# Clone your repository
git clone https://github.com/Rohitwangnekar/Indian-stock-market-trading-app.git

# Navigate to project directory
cd Indian-stock-market-trading-app
```

### 5. Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) at the beginning of your command prompt
```

### 6. Install Python Dependencies

#### Option A: Using Pipenv (Recommended)
```bash
# Install pipenv
pip install pipenv

# Install dependencies from Pipfile
pipenv install

# Activate pipenv shell
pipenv shell
```

#### Option B: Using pip with requirements.txt
```bash
# If you don't have requirements.txt, create it from Pipfile
pip install pipenv
pipenv requirements > requirements.txt

# Install dependencies
pip install -r requirements.txt
```

### 7. Set Up Environment Variables
```bash
# Copy sample environment file
cp sample.env .env

# Edit the .env file with your credentials
nano .env
```

**⚠️ IMPORTANT**: Replace ALL placeholder values in `.env` file:

```bash
# Example .env configuration
SECRET_KEY="your_super_secret_key_here_generate_a_new_one"
ALPHA_VANTAGE_API_KEY="your_alpha_vantage_api_key"
NEWS_API_KEY="your_news_api_key"
RAZORPAY_KEY_ID="your_razorpay_key_id"
RAZORPAY_KEY_SECRET="your_razorpay_key_secret"
```

### 8. Initialize Database
```bash
# Set Flask app environment variable
export FLASK_APP=application.py

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 9. Run the Application
```bash
# For development
python3 application.py

# OR using Flask command
flask run

# OR using Gunicorn (production)
gunicorn --bind 0.0.0.0:5000 application:app
```

### 10. Access the Application
- Open your web browser
- Go to: `http://localhost:5000`
- Register a new account and start trading!

## 🔧 Configuration Options

### Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

### Production Mode with Gunicorn
```bash
# Install gunicorn if not already installed
pip install gunicorn

# Run with multiple workers
gunicorn --bind 0.0.0.0:5000 --workers 4 application:app

# Run in background
nohup gunicorn --bind 0.0.0.0:5000 --workers 4 application:app > app.log 2>&1 &
```

### Using PostgreSQL (Optional)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE indian_stock_app;
CREATE USER stock_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE indian_stock_app TO stock_user;
\q

# Update .env file
DATABASE_URL="postgresql://stock_user:your_password@localhost/indian_stock_app"
```

## 🌐 Setting Up as System Service (Optional)

Create a systemd service to run the app automatically:

### 1. Create Service File
```bash
sudo nano /etc/systemd/system/indian-stock-app.service
```

### 2. Add Service Configuration
```ini
[Unit]
Description=Indian Stock Market Trading App
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Indian-stock-market-trading-app
Environment=PATH=/path/to/Indian-stock-market-trading-app/venv/bin
ExecStart=/path/to/Indian-stock-market-trading-app/venv/bin/gunicorn --bind 0.0.0.0:5000 application:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable indian-stock-app
sudo systemctl start indian-stock-app
sudo systemctl status indian-stock-app
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied Error
```bash
sudo chown -R $USER:$USER ~/Indian-stock-market-trading-app
chmod +x application.py
```

#### 2. Python Module Not Found
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Database Connection Error
```bash
# Check if database file exists
ls -la finance.db

# Recreate database
rm finance.db
flask db upgrade
```

#### 4. Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 PID_NUMBER

# Or use different port
flask run --port 8000
```

#### 5. API Key Issues
- Verify all API keys are correctly set in `.env`
- Check API key validity and limits
- Ensure `.env` file is in the project root directory

### Check Logs
```bash
# View application logs
tail -f app.log

# View system service logs
sudo journalctl -u indian-stock-app -f
```

## 🔒 Security Recommendations

1. **Firewall Setup**
```bash
sudo ufw enable
sudo ufw allow 22    # SSH
sudo ufw allow 5000  # Your app
```

2. **Keep System Updated**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Use Strong Passwords**
- Generate strong secret keys
- Use complex database passwords
- Regularly rotate API keys

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Gunicorn Documentation](https://gunicorn.org/)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs
3. Verify all environment variables
4. Ensure all dependencies are installed
5. Check API key validity

## 🎉 Success!

Once everything is running, you should see:
- ✅ Application accessible at `http://localhost:5000`
- ✅ Database initialized and working
- ✅ API integrations functional
- ✅ Indian stock data loading properly

Happy Trading! 🚀📈