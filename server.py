from flask import Flask, render_template, request
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
import os



app=Flask(__name__)
app.config['SECRET_KEY']="shbfihsbcaicbia1217"

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", "sqlite:///expenses.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin,db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    username:Mapped[str]=mapped_column(String,nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False)
    password:Mapped[str]=mapped_column()
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        pass

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    return render_template("register.html")

@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/add_expenses")
def add_expense():
    render_template("add_expense.html")

@app.route("/logout")
def logout():
    pass

@app.route("/charts")
def load_charts():
    return render_template("charts.html")

@app.route("/tables")
def load_tables():
    return render_template("tables.html")
if __name__ == "__main__":
    app.run(debug=True, port=5003)