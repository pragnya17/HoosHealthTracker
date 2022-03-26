from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/entry", methods=["POST", "GET"])
def entry():
    if request.method == "POST":
        # Example of retrieving data from form
        date = request.form['date']
        print(date)
    return render_template("entry.html")

@app.route("/current_week")
def current_week():
    return "Weekly progress"


# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)