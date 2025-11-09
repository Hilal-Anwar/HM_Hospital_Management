from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

# create the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
db = SQLAlchemy(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


with app.app_context():
    db.create_all()


# Redirect root to /user
@app.route('/')
def index():
    return render_template("admin_view.html")


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("list.html", users=users)


@app.route("/user/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_list"))
        else:
            return render_template("login.html")
    except Exception as e:
        return render_template("error.html")
@app.route("/user/register", methods=["GET", "POST"])
def user_register():
    try:
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_list"))
        else:
            return render_template("register.html")
    except Exception as e:
        return render_template("error.html")

@app.route("/user/<int:id>/edit", methods=["POST", "GET"])
def user_edit(id):
    user = db.session.query(User).get(id)
    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("user_list"))
    return render_template("edit.html", user=user)


@app.route("/user/<int:id>/delete")
def user_delete(id):
    user = db.get_or_404(User, id)
    print(user, request.method)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user_list"))


if __name__ == '__main__':
    app.run()
