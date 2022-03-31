from flask import Flask
from flask import render_template, request, redirect, url_for
import db
import nutr_calc


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
    # Retrieve food and nutrient info from database
    food = db.get_food(food_id)
    nutrients = db.get_nutrients(food_id)

    # The data has some repetitiveness in how it displays serving size in
    # the household_serving_fulltext and serving_size columns, so here we eliminate that
    if str(int(food['serving_size'])) in food['household_serving_fulltext'] or str(food['serving_size']) in food['household_serving_fulltext']:
        ss = food['household_serving_fulltext']
    else:
        ss = food['household_serving_fulltext'] + " (" + str(food['serving_size']) + "g)"

    # Our food info gives a "household" serving size, but our nutrient info is per 100g
    # So here we update the nutrients to reflect the household serving size
    # If not possible to convert between the two serving sizes, we just update the displayed serving size to 100g
    if food['serving_size_unit'] == 'g':
        nutrients = nutr_calc.get_updated_nutrients(nutrients, food['serving_size'])
    else:
        ss = "100g"

    # Compute and store number of calories derived from macronutrients
    nutrients['calories'] = nutr_calc.get_calories(nutrients['fat'], nutrients['carb'], nutrients['protein'])
    
    # Compute % daily values for each macronutrient
    daily_values = nutr_calc.get_daily_values(nutrients)

    return render_template("food_nutrition.html", food=food, nutrients=nutrients, daily_values=daily_values, ss=ss)
 

@app.route("/current_week")
def current_week():
    return "Weekly progress"


# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)