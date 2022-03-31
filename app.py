from flask import Flask
from flask import render_template, request, redirect, url_for
import db


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

@app.route("/food_search", methods=["POST", "GET"])
def food_search():
    if request.method == "GET":
        return render_template("food_search.html")

    if request.method == "POST":
        return redirect(url_for('search_result'))
    

@app.route("/search_result", methods=["POST"])
def search_result():
    if request.method == "POST":
        food_to_search = request.form['food_to_search']
        food_results = db.get_foods(food_to_search)

        return render_template("search_result.html", food_to_search=food_to_search, food_results=food_results)

@app.route("/nutrition_info/<food_id>")
def nutrition_info(food_id):
    food = db.get_food(food_id)
    nutrition = db.get_nutrition(food_id)
    nutrition['calories'] = round(9*nutrition['fat'] + 4*(nutrition['carb'] + nutrition['protein']))
    daily_values = {
        'calories': round(nutrition['calories']/2000 * 100),
        'fat': round(nutrition['fat']/65 * 100),
        'carb': round(nutrition['carb']/300 * 100),
        'protein': round(nutrition['protein']/50 * 100)
    }
    return render_template("food_nutrition.html", food=food, nutrition=nutrition, daily_values=daily_values)
 

@app.route("/current_week")
def current_week():
    return "Weekly progress"


# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)