from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from db_secrets import secrets
import db
import hashlib
import nutr_calc
from datetime import datetime, timedelta

app = Flask(__name__)

user_id = -1 # -1 means no one is logged in

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

    return render_template("sign_up.html")


@app.route("/main")
def main():
    if user_id != -1:
        emotionResult = db.getEmotionEntry(user_id, datetime.now().strftime('%Y-%m-%d'))
        exerciseResult = db.getExerciseEntry(user_id, datetime.now().strftime('%Y-%m-%d'))
        sleepResult = db.getSleepEntry(user_id, datetime.now().strftime('%Y-%m-%d'))
        foodResult = db.getFoodEntry(user_id, datetime.now().strftime('%Y-%m-%d'))

        # get these from main.html? for update/delete
        comment = 0
        mood = 0
        # print(mood)
        intensity = 0
        duration = 0
        type = 0
        sleep = 0
        calories = 0
        fat = 0
        carbs = 0
        protein = 0
        weight = 0
 
        # for update/delete buttons on main.html
        if request.method == "POST":              
            # if updating an entry
            if request.form["btnAction"] == "Update":
                db.updateEmotionEntry(user_id, datetime.now().strftime('%Y-%m-%d'), comment, mood)
                db.updateExerciseEntry(user_id,  datetime.now().strftime('%Y-%m-%d'), comment, intensity, duration, type)
                db.updateSleepEntry(user_id, datetime.now().strftime('%Y-%m-%d'), comment, sleep)
                db.updateFoodEntry(user_id, datetime.now().strftime('%Y-%m-%d'), comment, calories, fat, carbs, protein, weight)
           
            # if deleting an entry
            if request.form["btnAction"] == "Delete":
                db.deleteEmotionEntry(user_id,   datetime.now().strftime('%Y-%m-%d'))
                db.deleteExerciseEntry(user_id, datetime.now().strftime('%Y-%m-%d'))
                db.deleteSleepEntry(user_id,  datetime.now().strftime('%Y-%m-%d'))
                db.deleteFoodEntry(user_id,  datetime.now().strftime('%Y-%m-%d'), calories, fat, carbs, protein)

        return render_template("main.html", emotionResult=emotionResult, exerciseResult=exerciseResult, sleepResult=sleepResult, foodResult=foodResult)
    
    else:
        return redirect(url_for('login'))


@app.route("/profile")
def profile():
    if user_id != -1:
        first_name, last_name, height, date_of_birth = db.get_user(user_id)
        return render_template("profile.html", first_name=first_name, last_name=last_name,
                               height=height, date_of_birth=date_of_birth)
    else:
        return redirect(url_for('login'))


@app.route("/entry", methods=["POST", "GET"])
def entry():
    global user_id

    if user_id == -1:
        return redirect(url_for('login'))
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
        # food entry
        calories = request.form['calories']
        fat = request.form['fat']
        carbs = request.form['carbs']
        protein = request.form['protein']
        weight = request.form['weight']

        db.storeEmotionEntry(user_id, date, comment, mood)
        db.storeSleepEntry(user_id, date, comment, sleep)
        db.storeExerciseEntry(user_id, date, comment, intensity, duration, type)
        db.storeFoodEntry(user_id, date, comment, calories, fat, carbs, protein, weight)
        
    return render_template("entry.html")
  
@app.route("/food_update/<date>", methods=["POST", "GET"])
def food_entry_update(date):
    if request.method == "GET":
        foodResult = db.get_single_food_entry(user_id, date)    
        return render_template("food_update.html", date=date, foodResult=foodResult)

    if request.method == "POST":
        if request.form["btnAction"] == "UPDATE":
            calories = request.form['calories']
            carbs = request.form['carbs']
            protein = request.form['protein']
            fat = request.form['fat']
            db.updateFoodEntry(user_id, date, "dummy_str", calories, fat, carbs, protein, 10)

        if request.form["btnAction"] == "DELETE":
            db.deleteFoodEntry(user_id, date)

        return redirect(url_for('main'))

@app.route("/mood_update/<date>", methods=["POST", "GET"])
def mood_entry_update(date):
    if request.method == "GET":
        moodResult = db.get_single_emotion_entry(user_id, date)    
        return render_template("mood_update.html", date=date, moodResult=moodResult)
    
    if request.method == "POST":
        if request.form["btnAction"] == "UPDATE":
            mood = request.form['mood']
            comments = request.form['comments']
            db.updateEmotionEntry(user_id, date, comments, mood)

        if request.form["btnAction"] == "DELETE":
            db.deleteEmotionEntry(user_id, date)

        return redirect(url_for('main'))

@app.route("/exercise_update/<date>", methods=["POST", "GET"])
def exercise_entry_update(date):
    if request.method == "GET":
        exerciseResult = db.get_single_exercise_entry(user_id, date)    
        return render_template("exercise_update.html", date=date, exerciseResult=exerciseResult)
    
    if request.method == "POST":
        if request.form["btnAction"] == "UPDATE":
            intensity = request.form['exercise_intensity']
            duration = request.form['exercise_duration']
            type = request.form['exercise_type']
            db.updateExerciseEntry(user_id, date, "dummy_str", intensity, duration, type)

        if request.form["btnAction"] == "DELETE":
            db.deleteExerciseEntry(user_id, date)

        return redirect(url_for('main'))

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
 

# For debugging - just run file from terminal and any saved changes will be updated in browser
# without having to restart the program.
if __name__ == '__main__':
    app.run(debug=True)