from flask import Flask
from flask import render_template, request, redirect, url_for
from db_secrets import secrets
import db


app = Flask(__name__)

user_id = -1 # -1 means no is logged in

@app.route("/", methods=["POST", "GET"])
def login():
    global user_id

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = db.get_users_emails()

        for user in users:
            if email == user["email"] and password == user["password"]:
                user_id = user["user_id"]

    return render_template("login.html")

@app.route("/profile")
def profile():
    if user_id != -1:
        return render_template("profile.html")
    else:
        return redirect(url_for('login'))

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