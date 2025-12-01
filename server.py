from functools import wraps
from os import abort
from datetime import datetime
from flask import Flask, render_template, request,redirect,flash,url_for
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, func
import os

from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config['SECRET_KEY']="shbfihsbcaicbia1217"

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)


def login_required_custom(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the user is NOT authenticated
        if not current_user.is_authenticated:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function


class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", "sqlite:///expenses.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin,db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    first_name:Mapped[str]=mapped_column(String,nullable=False)
    last_name:Mapped[str]=mapped_column(String,nullable=False)
    username:Mapped[str]=mapped_column(String,nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False)
    password:Mapped[str]=mapped_column(Integer,nullable=False)
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
        email=request.form.get("email")
        password=request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Your password was incorrect")
        else:
            flash("Your email was invalid")

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        first_name=request.form.get("first_name")
        last_name=request.form.get("last_name")
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("You have already signed up with this email")
            return redirect(url_for("login"))
        new_user=User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template("register.html")

@app.route("/home")
@login_required_custom
def index():
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar()
    return render_template("index.html",total_expenses=total_expenses)

@app.route("/add_expense",methods=["POST","GET"])
@login_required_custom
def add_expense():
    if request.method=="POST":
        category=request.form.get("category")
        date=request.form.get("date")
        amount=request.form.get("amount")
        description=request.form.get("note")
        user_id=current_user.id
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        new_expense = Expense(
            user_id=user_id,
            category=category,
            amount=float(amount),
            date=date_obj,
            description=description
        )
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/logout")
@login_required_custom
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/charts")
@login_required_custom
def load_charts():
    return render_template("charts.html")

@app.route("/tables")
@login_required_custom
def load_tables():
    return render_template("tables.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)