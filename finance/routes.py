import flask
import flask_session
import requests
from werkzeug import security, exceptions
from finance import app, db
from . import helpers
from .models import User, Transaction

from flask import Flask, request, render_template, jsonify, redirect, url_for

import logging
from .models import Contact
from flask import flash


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Jinja2 custom filters
app.jinja_env.filters["inr"] = helpers.inr
app.jinja_env.filters["lookup"] = helpers.lookup


# Apply flask_session to app
flask_session.Session(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@helpers.login_required
def index():
    user = User.query.get(flask.session.get("user_id"))
    portfolio = helpers.get_portfolio()
    for stock in portfolio:
        stock["price"] = helpers.lookup(stock["symbol"])["price"]

    return flask.render_template("index.html", portfolio=portfolio, cash=user.cash)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        confirmation = flask.request.form.get("confirmation")


        if not username:
            return helpers.apology("must provide username", 401)
        elif not password:
            return helpers.apology("must provide password", 401)
        elif not confirmation:
            return helpers.apology("must provide confirmation password", 401)
        elif password != confirmation:
            return helpers.apology("password and confirmation password must be same", 401)


        user_check = User.query.filter_by(username=username).first()
        if user_check is None:
            user = User(username=username, hash=security.generate_password_hash(password))
            db.session.add(user)
            db.session.commit()


            flask.session["user_id"] = user.id
            flask.flash("Wow, we got a new user. You have successfully registered 😀", "success")
            return flask.redirect(flask.url_for("index"))
        else:
            return helpers.apology("username already taken", 401)


    elif flask.request.method == "GET" and flask.session.get("user_id") is not None:
        flask.flash("Ummm, you have already registered 😉", "info")
        return flask.redirect(flask.url_for("index"))


    return flask.render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")


        if not username:
            return helpers.apology("must provide username", 401)
        elif not password:
            return helpers.apology("must provide password", 401)


        user = User.query.filter_by(username=username).first()
        if user is None or not security.check_password_hash(user.hash, password):
            return helpers.apology("invalid username or password", 401)


        flask.session["user_id"] = user.id
        flask.flash("Welcome again! You have successfully logged in 😀", "success")
        return flask.redirect(flask.url_for("index"))


    elif flask.request.method == "GET" and flask.session.get("user_id") is not None:
        flask.flash("Don't be greedy, you are already logged in 😉", "info")
        return flask.redirect(flask.url_for("index"))


    return flask.render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """Log user out."""
    flask.session.clear()
    flask.flash("You have successfully logged out. It's bad to see you go. We'll miss you 😔", "success")
    return flask.redirect(flask.url_for("index"))


@app.route("/quote", methods=["GET", "POST"])
@helpers.login_required
def quote():
    """Get stock quote (via helpers.lookup)."""
    quote = None
    if flask.request.method == "POST":
        symbol = flask.request.form.get("symbol")
        if not symbol:
            return helpers.apology("must provide symbol", 400)


        quote = helpers.lookup(symbol)
        if quote is None:
            flask.flash(f"Couldn't get quote for \"{symbol}\". Please re-check spelling and try again.", "danger")


    return flask.render_template("quote.html", quote=quote)


@app.route("/buy", methods=["GET", "POST"])
@helpers.login_required
def buy():
    """Buy shares of stock."""
    if flask.request.method == "POST":
        symbol = flask.request.form.get("symbol")
        shares = flask.request.form.get("shares")


        if not symbol:
            return helpers.apology("must provide symbol", 400)
        if not shares:
            return helpers.apology("must provide shares", 400)


        quote = helpers.lookup(symbol)
        if quote is None:
            flask.flash(f"Symbol \"{symbol}\" is invalid. Please re-check spelling and try again.", "danger")
        else:
            cost = float(int(shares) * quote["price"])
            user_data = User.query.get(flask.session.get("user_id"))


            if user_data.cash >= cost:
                transaction = Transaction(user_id=user_data.id, company_name=quote["name"], company_symbol=quote["symbol"], shares=int(shares), price=quote["price"], trans_type="purchase")
                db.session.add(transaction)
                user_data.cash -= cost
                db.session.commit()
                flask.flash("Purchase successful 🤑", "info")
                return flask.redirect(flask.url_for("index"))
            else:
                flask.flash(f"You don't have enough cash. Money required for purchase is {helpers.inr(cost)} and you have {helpers.inr(user_data.cash)} 😥", "info")


    return flask.render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@helpers.login_required
def sell():
    """Sell shares of stock."""
    portfolio = helpers.get_portfolio()

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            flash("must provide symbol", "danger")
            return redirect(url_for("sell"))
        if not shares:
            flash("must provide shares", "danger")
            return redirect(url_for("sell"))
        
        try:
            shares = int(shares)
        except ValueError:
            flash("Shares must be a valid number", "danger")
            return redirect(url_for("sell"))

        if shares <= 0:
            flash("Shares must be a positive number", "danger")
            return redirect(url_for("sell"))

        stock_info = helpers.lookup(symbol)
        if stock_info is None:
            flash("Symbol not found", "danger")
            return redirect(url_for("sell"))

        for stock in portfolio:
            if symbol == stock["symbol"]:
                if shares <= stock["shares"]:
                    user = User.query.get(session.get("user_id"))
                    price = stock_info["price"]

                    transaction = Transaction(
                        user_id=user.id,
                        company_name=stock["name"],
                        company_symbol=stock["symbol"],
                        shares=shares,
                        price=price,
                        trans_type="sale"
                    )
                    db.session.add(transaction)
                    user.cash += price * shares
                    db.session.commit()

                    flash("Successfully sold 🙌", "success")
                    return redirect(url_for("index"))
                else:
                    flash("You don't have enough shares", "danger")
                break
        else:
            flash("Symbol not found in your portfolio", "danger")

    return render_template("sell.html", portfolio=portfolio)


@app.route("/history", methods=["GET"])
@helpers.login_required
def history():
    """Show history of transactions."""
    user_id = flask.session.get("user_id")
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.transacted_at.desc()).all()
    return flask.render_template("history.html", transactions=transactions)


@app.route("/api/check/<string:username>", methods=["GET"])
def check(username):
    """Return true if username available, else false, in JSON format."""
    result = User.query.filter_by(username=username).first()
    return flask.jsonify(is_username_available=result is None)


def errorhandler(e):
    """Handle error."""
    if not isinstance(e, exceptions.HTTPException):
        e = exceptions.InternalServerError()
    return helpers.apology(e.name, e.code)


for code in exceptions.default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/news")
@helpers.login_required
def news():
    """Display Indian stock market news."""
    news = helpers.fetch_stock_market_news()
    return flask.render_template("news.html", news=news)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print(request.form)  # Print out the form data to debug
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        query = request.form.get('query')


        # Debugging statements
        print(f"Received first_name: {first_name}")
        print(f"Received email: {email}")
        print(f"Received phone_number: {phone_number}")
        print(f"Received query: {query}")


        if not first_name or not email or not phone_number or not query:
            flash('Please fill out all required fields.')
            return redirect(url_for('contact'))


        new_contact = Contact(first_name=first_name, email=email, phone_number=phone_number, query=query)
        db.session.add(new_contact)
        try:
            db.session.commit()
            flash('Your query has been submitted.')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.')
            print(e)
        return redirect(url_for('contact'))
    return render_template('contact.html')

from flask import jsonify, request, session, render_template
from .models import User, Order  # Ensure correct import paths
from . import app, db, helpers
import razorpay

@app.route('/payment')
def payment():
    razorpay_key = app.config.get('RAZORPAY_KEY_ID')
    if not razorpay_key:
        raise KeyError('RAZORPAY_KEY_ID is not set in the configuration')
    return render_template('payment.html', razorpay_key=razorpay_key)

@app.route('/create_order', methods=['POST'])
@helpers.login_required
def create_order():
    user_id = session.get('user_id')
    amount = request.json.get('amount')

    if not amount:
        return jsonify({'error': 'Amount is required'}), 400

    client = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

    order = Order(user_id=user_id, order_id=payment['id'], amount=amount, status='created')
    db.session.add(order)
    db.session.commit()

    return jsonify(payment)

@app.route('/verify_payment', methods=['POST'])
@helpers.login_required
def verify_payment():
    data = request.form.to_dict()
    client = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))

    try:
        client.utility.verify_payment_signature(data)
        order = Order.query.filter_by(order_id=data['razorpay_order_id']).first()
        if order:
            order.status = 'paid'
            db.session.commit()
        return jsonify({'status': 'Payment verified successfully'}), 200
    except:
        return jsonify({'status': 'Payment verification failed'}), 400



from flask import Flask, render_template
@app.route('/market_overview')
def market_overview():
    return render_template('market_overview.html')

@app.route('/crypto_chart')
def crypto_chart():
    return render_template('crypto_chart.html')

if __name__ == '__main__':
    app.run(debug=True)



