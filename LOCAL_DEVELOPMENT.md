# 🏠 Local Development Setup - Indian Stock Market Trading App

This guide shows you how to run the app locally with embedded API keys for convenience.

## ⚠️ IMPORTANT WARNINGS

- **FOR LOCAL DEVELOPMENT ONLY** - Never deploy these files to production
- **API KEYS INCLUDED** - The local files contain actual API keys for testing
- **NOT FOR PUBLIC REPOS** - These files are automatically excluded from Git
- **REPLACE WITH YOUR OWN** - Use your own API keys for better functionality

## 🚀 Quick Local Setup

### Method 1: Using the Local Runner (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Rohitwangnekar/Indian-stock-market-trading-app.git
cd Indian-stock-market-trading-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the local development server
python3 run_local.py
```

### Method 2: Manual Configuration

```bash
# 1. Use the local application file
python3 application_local.py
```

## 🔧 What's Included in Local Development

### Pre-configured API Keys:
- **Razorpay Test Keys**: Ready for payment testing
- **Alpha Vantage Demo Key**: For stock data (limited requests)
- **News API Placeholder**: Replace with your own key
- **Development Secret Key**: For Flask sessions

### Features:
- ✅ **No Environment Setup Required**
- ✅ **Database Auto-Creation**
- ✅ **Debug Mode Enabled**
- ✅ **Hot Reloading**
- ✅ **Detailed Error Messages**

## 📁 Local Development Files

The following files contain embedded API keys for local development:

```
📂 Local Development Files (Git Ignored)
├── config_local.py           # Configuration with API keys
├── application_local.py       # Local app runner
├── run_local.py              # Development server script
└── finance/__init___local.py  # Local finance module
```

## 🌐 Accessing Your Local App

Once started, your app will be available at:
- **URL**: http://localhost:5000
- **Debug Mode**: Enabled
- **Auto-Reload**: Enabled

## 🔄 Development vs Production

| Feature | Local Development | Production |
|---------|------------------|------------|
| API Keys | Embedded in code | Environment variables |
| Database | SQLite | PostgreSQL recommended |
| Debug Mode | Enabled | Disabled |
| Security | Basic | Enhanced |
| Performance | Development | Optimized |

## 🛠️ Customizing Local Development

### 1. Replace API Keys in `config_local.py`:

```python
# Replace these with your own API keys for better functionality
RAZORPAY_KEY_ID = 'your_razorpay_key_here'
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_key_here'
NEWS_API_KEY = 'your_news_api_key_here'
```

### 2. Database Configuration:

```python
# Use different database for local development
SQLALCHEMY_DATABASE_URI = "sqlite:///local_finance.db"
```

### 3. Development Settings:

```python
# Customize development behavior
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
```

## 🔒 Security Notes

### Local Development Security:
- ✅ Files are Git-ignored (won't be committed)
- ✅ Only accessible from localhost
- ✅ Test API keys used (limited functionality)
- ⚠️ Not suitable for production use

### When Moving to Production:
1. Use the regular `application.py`
2. Set up environment variables
3. Use production-grade database
4. Enable proper security measures

## 🐛 Troubleshooting Local Development

### Common Issues:

#### 1. **Port Already in Use**
```bash
# Kill process on port 5000
sudo lsof -i :5000
sudo kill -9 PID_NUMBER

# Or use different port
python3 run_local.py --port 8000
```

#### 2. **Module Import Errors**
```bash
# Ensure you're in the project directory
cd Indian-stock-market-trading-app

# Install dependencies
pip install -r requirements.txt
```

#### 3. **Database Issues**
```bash
# Remove database and recreate
rm finance.db
python3 run_local.py
```

#### 4. **API Key Issues**
- Check that API keys in `config_local.py` are valid
- Alpha Vantage demo key has limited requests
- Get your own API keys for unlimited access

## 📊 Local Development Features

### What Works Out of the Box:
- ✅ User registration and login
- ✅ Basic stock lookup
- ✅ Portfolio management
- ✅ Transaction history
- ✅ Payment integration (test mode)

### What Needs Your API Keys:
- 📈 Real-time stock data (Alpha Vantage)
- 📰 Market news (News API)
- 💳 Live payments (Razorpay production)

## 🚀 Next Steps

### For Local Development:
1. Run `python3 run_local.py`
2. Open http://localhost:5000
3. Register an account
4. Start trading with demo data!

### For Production Deployment:
1. Follow the [Ubuntu Setup Guide](UBUNTU_SETUP.md)
2. Use environment variables for API keys
3. Configure production database
4. Set up proper security measures

## 🎉 Happy Local Development!

Your local development environment is now ready with:
- 🔑 Pre-configured API keys
- 🗄️ Auto-created database
- 🔄 Hot reloading
- 🐛 Debug mode
- 📱 Responsive interface

Start coding and testing your Indian Stock Market Trading App locally! 🇮🇳📈