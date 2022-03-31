from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from db_secrets import secrets
import db
import hashlib

app = Flask(__name__)

user_id = -1 # -1 means no is logged in


@app.route("/", methods=["POST", "GET"])
def login():
    global user_id

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        users = db.get_users_emails()

        for user in users:
            if email == user["email"] and hashed_password == user["password"]:
                user_id = user["user_id"]
                return redirect(url_for('main'))

    return render_template("login.html")


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        height = request.form['height']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']
        password = request.form['password']

        success = db.add_user(first_name, last_name, height, date_of_birth, email, password)

        # if success:
        #     flash(request, "You are now signed up! Please log in to your new account below.")
        #     return redirect(url_for('sign_up'))

    return render_template("sign_up.html")


@app.route("/main")
def main():
    if user_id != -1:
        return render_template("main.html")
    else:
        return redirect(url_for('login'))


@app.route("/profile")
def profile():
    if user_id != -1:
        first_name, last_name, height, date_of_birth = db.get_user(user_id)
        return render_template("profile.html", first_name=first_name, last_name=last_name,
                               height="height", date_of_birth=date_of_birth)
    else:
        return redirect(url_for('login'))


@app.route("/entry", methods=["POST", "GET"])
def entry():
    if request.method == "POST":
        # Example of retrieving data from form
        date = request.form['date']
        print(date)
    return render_template("entry.html")

@app.route("/current_week")
def current_week():
    if user_id != -1:
        return "Weekly progress"
    else:
        return redirect(url_for('login'))


# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)