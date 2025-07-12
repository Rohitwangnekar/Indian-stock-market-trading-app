import os
import requests
import urllib
from finance import db
from flask import redirect, render_template, request, session, flash
from functools import wraps
from sqlalchemy.sql import func
from .models import Transaction
import yfinance as yf

def apology(message, code):
    """Render message and error code as an apology to user."""
    def escape(s):
        """Escape special characters for URLs."""
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(message), bottom=("error " + str(code))), code

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""
    try:
        api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("API key for Alpha Vantage is not set.")
        response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={urllib.parse.quote_plus(symbol)}.BSE&apikey={api_key}")
        response.raise_for_status()

        # Debugging: Print the response content
        print("API Response:", response.content)

        quote = response.json()["Global Quote"]
        return {
            "name": symbol,  # Alpha Vantage doesn't provide company names in GLOBAL_QUOTE
            "price": float(quote["05. price"]),
            "symbol": symbol
        }
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return None
    except (KeyError, TypeError, ValueError) as e:
        print("Error processing data:", e)
        return None

def get_portfolio():
    """Fetch the portfolio of stocks the user has."""
    user_id = session.get("user_id")
    if not user_id:
        return []

    purchases = db.session.query(Transaction.company_name, Transaction.company_symbol, func.sum(Transaction.shares).label("shares")).filter_by(user_id=user_id, trans_type="purchase").group_by(Transaction.company_symbol, Transaction.company_name).order_by(Transaction.company_symbol).all()
    sales = db.session.query(Transaction.company_name, Transaction.company_symbol, func.sum(Transaction.shares).label("shares")).filter_by(user_id=user_id, trans_type="sale").group_by(Transaction.company_symbol, Transaction.company_name).order_by(Transaction.company_symbol).all()

    portfolio = []
    sales_dict = {sale.company_symbol: sale.shares for sale in sales}

    for purchase in purchases:
        sales_shares = sales_dict.get(purchase.company_symbol, 0)
        net_shares = purchase.shares - sales_shares
        if net_shares > 0:
            portfolio.append({
                "name": purchase.company_name,
                "symbol": purchase.company_symbol,
                "shares": int(net_shares)
            })
    return portfolio

def inr(value):
    """Format value as INR."""
    if value is None:
        return "₹0.00"
    return f"₹{value:,.2f}"

def fetch_stock_market_news():
    """Fetch Indian stock market news."""
    news_api_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "business",
        "country": "in",
        "apiKey": os.environ.get("NEWS_API_KEY")
    }
    try:
        response = requests.get(news_api_url, params=params)
        response.raise_for_status()
        news_data = response.json()
        return news_data.get("articles", [])
    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def fetch_stock_price(symbol):
    """Fetch current stock price using Alpha Vantage API."""
    try:
        api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("API key for Alpha Vantage is not set.")
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={urllib.parse.quote_plus(symbol)}.BSE&apikey={api_key}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['Global Quote']['05. price'])
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")
        return None
