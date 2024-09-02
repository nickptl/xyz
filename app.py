from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///noobauth.db"
app.secret_key = "something"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String())

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        # self.password=password

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        # return password


with app.app_context():
    db.create_all()


@app.route('/')
def index2():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # session["name"]=user.name
            session["email"] = user.email
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid User Ho tum")

    # return "Hello Flask with python"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # return "Hello Flask with python"
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/index")
def index():
    if session["email"]:
        user = User.query.filter_by(email=session["email"]).first()
        return render_template("index.html", user=user)
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("email", None)  # remove username from the session if
    return redirect('/')

@app.route('/about')
def About():
    return render_template('about.html') 

@app.route('/service')
def Service():
    return render_template('service.html') 

@app.route('/contect')
def Contact():
    return render_template('contect.html')

@app.route('/index')
def Home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)