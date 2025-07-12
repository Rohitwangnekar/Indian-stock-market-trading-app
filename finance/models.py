import datetime
from finance import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    hash = db.Column(db.String(128), nullable=False)
    cash = db.Column(db.Float, default=10000.00, nullable=False)

    transactions = db.relationship("Transaction", back_populates="user")
    orders = db.relationship("Order", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
   
    # Many to one relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    user = db.relationship("User", back_populates="transactions")

    company_name = db.Column(db.String(128), index=True)
    company_symbol = db.Column(db.String(128), index=True, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    trans_type = db.Column(db.String(128), index=True, nullable=False)
    transacted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    query = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.first_name}>'

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="orders")

    order_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='created')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id, order_id, amount, status='created'):
        self.user_id = user_id
        self.order_id = order_id
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f'<Order {self.order_id}>'
