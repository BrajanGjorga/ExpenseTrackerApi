from flask import Flask, render_template, request




app=Flask(__name__)
app.config['SECRET_KEY']="shbfihsbcaicbia1217"



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

if __name__ == "__main__":
    app.run(debug=True, port=5003)