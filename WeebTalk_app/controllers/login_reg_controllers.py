from WeebTalk_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from WeebTalk_app.models.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/weebtalk/login')
def login():
    if "logged_in" in session:
        return redirect('/weebtalk')
    if "errors" in session and session["errors"] == True:
        email = session.pop("email", None)
        session["errors"] = False
        return render_template("login.html", email=email)
    return render_template('login.html')

@app.route('/weebtalk/login/process', methods=['POST'])
def process_login():
    if not Users.validate_login(request.form):
        session["errors"] = True
        session["email"] = request.form["email"]
        return redirect('/weebtalk/login')
    else:
        session["logged_in"] = Users.get_one_by_email(request.form["email"]).id
        return redirect('/weebtalk')

@app.route('/weebtalk/register')
def render_register():
    if "logged_in" in session:
        return redirect('/weebtalk')
    if "errors" in session and session["errors"] == True:
        username = session.pop("first", None)
        birthday = session.pop("birthday", None)
        email = session.pop("email", None)
        session["errors"] = False
        return render_template('register.html', username=username, birthday=birthday, email=email)
    return render_template('register.html')

@app.route('/weebtalk/register/process', methods=["POST"])
def process_register():
    if not Users.validate_user(request.form):
        session["errors"] = True
        session["username"] = request.form["username"]
        session["birthday"] = request.form["birthday"]
        session["email"] = request.form["email"]
        return redirect("/weebtalk/register")
    else:
        data = {
            "username": request.form["username"],
            "birthday": request.form["birthday"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        Users.save(data)
        session["logged_in"] = Users.get_one_by_email(request.form["email"]).id
        return redirect('/weebtalk')

@app.route('/weebtalk/logout')
def logout():
    session.clear()
    return redirect('/weebtalk/login')