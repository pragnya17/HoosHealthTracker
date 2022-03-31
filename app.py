from flask import Flask
from flask import render_template, request
from db import *

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
        # Example of retrieving data from form (need both for every entry)
        date = request.form['date']
        comment = request.form['comments']

        # emotion entry
        mood = request.form['mood']
        # sleep entry
        sleep = request.form['sleep']
        # exercise entry
        intensity = request.form['exercise_intensity']
        duration = request.form['exercise_duration']
        type = request.form['exercise_type']
        # food entry/food entry nutritions
        calories = request.form['calories']
        fat = request.form['fat']
        carbs = request.form['carbs']
        protein = request.form['protein']
        weight = request.form['weight']


        user_id = 8

        # storeEmotionEntry(user_id, date, comment, mood)
        # storeSleepEntry(user_id, date, comment, sleep)
        # storeExerciseEntry(user_id, date, comment, intensity, duration, type)
        storeFoodEntry(user_id, date, comment, calories, fat, carbs, protein, weight)


        # print(get_users())
        # print(date)
        # print(comment)
        # print(mood)
        # print(sleep)
    return render_template("entry.html")

@app.route("/current_week")
def current_week():
    return "Weekly progress"


# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)