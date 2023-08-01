import datetime

from flask import Flask, render_template, request, url_for, redirect
from tables import CoffeeShop, User, Comment, db
from forms import RegisterForm, LoginForm, CommentForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_migrate import Migrate
from datetime import datetime
import bcrypt
import pendulum

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "very secret"
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

with app.app_context():
    db.create_all()

def time_ago(occurred_at):
    now = pendulum.instance(datetime.today())
    occurred_at = pendulum.instance(occurred_at)
    time_difference = now - occurred_at

    # Get the time components in seconds, minutes, hours, days, months, and years
    seconds = time_difference.in_seconds()
    minutes = time_difference.in_minutes()
    hours = time_difference.in_hours()
    days = time_difference.in_days()
    months = time_difference.in_months()
    years = time_difference.in_years()

    # Determine the appropriate unit of time to display
    if years >= 1:
        return f"{int(years)} {'year' if int(years) == 1 else 'years'} ago"
    elif months >= 1:
        return f"{int(months)} {'month' if int(months) == 1 else 'months'} ago"
    elif days >= 1:
        return f"{int(days)} {'day' if int(days) == 1 else 'days'} ago"
    elif hours >= 1:
        return f"{int(hours)} {'hour' if int(hours) == 1 else 'hours'} ago"
    elif minutes >= 1:
        return f"{int(minutes)} {'minute' if int(minutes) == 1 else 'minutes'} ago"
    else:
        return f"{int(seconds)} {'second' if int(seconds) == 1 else 'seconds'} ago"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/")
def home():
    print(datetime.today())
    users = User.query.all()

    for user in users:
        print(user.comments)
    cafes = CoffeeShop.query.all()
    for cafe in cafes:
        print("comments",cafe.comments)
    comments = Comment.query.all()
    for comment in comments:
        print(time_ago(comment.date))


    return render_template("index.html", cafes=cafes, cur_user=current_user)

@app.route("/liked")
#@login_required
def get_liked_cafes():
    if current_user.is_authenticated:
        liked_cafes = current_user.liked_cafes
        return render_template("index.html", cafes=liked_cafes, cur_user=current_user)
    else:
        return "You need to login or create an account first."

@app.route("/cafe/<cafe_id>", methods=["POST", "GET"])
def view_cafe(cafe_id):
    form = CommentForm()
    if request.method=="POST":
        print("comment received")
        content = request.form.get("content")
        user = current_user.get_id()
        new_comment = Comment(
            content=content,
            user=user,
            cafe=cafe_id,
            date=datetime.today()
        )

        with app.app_context():
            db.session.add(new_comment)
            db.session.commit()
    cafe = CoffeeShop.query.filter_by(id=cafe_id).first()
    form.content.data=""
    print(cafe)
    comments = Comment.query.order_by(Comment.date.desc()).all()
    print(comments)
    return render_template("cafe.html", form=form, cur_user=current_user, cafe=cafe,
                           comments=comments, time_ago=time_ago)

@app.route("/search", methods=["POST"])
def search():
    query=request.form.get("search")
    print(query)
    searched_cafes = CoffeeShop.query.filter(CoffeeShop.location.ilike(f'%{query}%')).all()

    return render_template("index.html",cafes=searched_cafes, cur_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    error=False
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get("email")).first()
        user_input_password = request.form.get("password")
        print(str(user.password))
        if bcrypt.hashpw(user_input_password.encode('utf-8'), user.password) == user.password \
                and user is not None:
            login_user(user)
            return redirect(url_for('home'))
        else:
            error="Your password or email-address was wrong!"
            return render_template("login.html", form=form, error=error, cur_user=current_user)

    return render_template("login.html", form=form, error=error, cur_user=current_user)


@app.route("/update_state/<new_id>/<state>", methods=["POST"])
def get_update(new_id, state):
    print("state", state)
    liked_cafe = CoffeeShop.query.filter_by(id=new_id).first()
    if state == "checked":
        current_user.liked_cafes.append(liked_cafe)

    if state == "unchecked":
        current_user.liked_cafes.remove(liked_cafe)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    error = False
    if request.method == "POST":
        posted_email = request.form.get("email")
        user = User.query.filter_by(email=posted_email).first()

        if user is not None:
            error = "An account with this email-address already exists."
            return render_template("register.html", form=form, error=error, cur_user=current_user)
        password_bytes = request.form.get("password").encode('utf-8')
        print(password_bytes)
        hashed_password = bcrypt.hashpw(password=password_bytes,
                                        salt=bcrypt.gensalt(rounds=12),
                                        )
        new_user = User(
            user_name=request.form.get("username"),
            password=hashed_password,
            email=request.form.get("email"),


        )
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
        cur_user = User.query.filter_by(email=request.form.get("email")).first()
        login_user(cur_user)

        return redirect(url_for('home'))
    return render_template("register.html", form=form, error=error, cur_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
