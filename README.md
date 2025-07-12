# Indian Stock Market Trading App 🇮🇳

A comprehensive stock trading web application built on Flask, specifically designed for the Indian stock market (NSE/BSE). This application provides real-time access to Indian equities, mutual funds, and market data.

## Features 📈

- **Indian Stock Market Integration**: Real-time stock prices from NSE (National Stock Exchange) and BSE (Bombay Stock Exchange)
- **Buy & Sell Orders**: Execute trades for Indian stocks with INR currency support
- **Portfolio Management**: Track your investments in Indian equities and mutual funds
- **Transaction History**: Complete history of all your stock purchases and sales
- **Market Data**: Live market data for Indian stocks, indices (Nifty 50, Sensex), and sectors
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Mobile-friendly interface for trading on the go

## Indian Market Features 🏦

- Support for NSE and BSE listed stocks
- INR currency formatting and calculations
- Indian market trading hours awareness
- Popular Indian stocks and indices tracking
- Integration with Indian financial data providers

## Technology Stack 💻

- **Backend**: Flask (Python)
- **Database**: SQLite/PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap
- **API**: Indian stock market data integration
- **Authentication**: Flask-Login

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- Git
- Ubuntu 18.04+ (for Linux users)

### Quick Setup Options

📋 **For Ubuntu Users**: Follow our detailed [Ubuntu Setup Guide](UBUNTU_SETUP.md)

📋 **For Other Platforms**: Continue with the installation steps below

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Indian-stock-market-trading-app.git
   cd Indian-stock-market-trading-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **⚠️ IMPORTANT: Set up API credentials**
   
   **DO NOT USE THE APP WITHOUT SETTING UP YOUR OWN API KEYS**
   
   a. Copy the sample environment file:
   ```bash
   cp sample.env .env
   ```
   
   b. Edit `.env` file and replace ALL placeholder values with your own credentials:
   
   - **Alpha Vantage API Key** (Required for stock data):
     - Get free API key: https://www.alphavantage.co/support/#api-key
     - Replace: `your_alpha_vantage_api_key_here`
   
   - **News API Key** (Required for market news):
     - Get free API key: https://newsapi.org/register
     - Replace: `your_news_api_key_here`
   
   - **Razorpay Credentials** (Required for payments):
     - Get credentials: https://dashboard.razorpay.com/app/keys
     - Replace: `your_razorpay_key_id_here` and `your_razorpay_key_secret_here`
   
   - **Secret Key** (Required for security):
     - Generate a strong secret key (32+ characters)
     - Replace: `your_super_secret_key_here_generate_a_new_one`

4. **Run the application**
   ```bash
   python application.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:5000`

## Security Notice 🔒

- **NEVER commit your `.env` file to version control**
- **NEVER share your API keys publicly**
- **Always use environment variables for sensitive data**
- The `sample.env` file contains only placeholder values - you MUST replace them with your own credentials

## Target Markets 📊

- NSE (National Stock Exchange of India)
- BSE (Bombay Stock Exchange)
- Indian mutual funds and ETFs
- Popular Indian stocks (TCS, Reliance, HDFC Bank, etc.)
