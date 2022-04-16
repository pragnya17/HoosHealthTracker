import pymysql.cursors
from db_secrets import secrets
import hashlib
import datetime as dt

# Connect to the database
connection = pymysql.connect(host= secrets['host'],
                             user= secrets['user'],
                             password= secrets['password'],
                             database= secrets['database'],
                             cursorclass=pymysql.cursors.DictCursor)


def get_users_emails():
    with connection.cursor() as cursor:
        query = "SELECT * FROM UserProfileEmails;"
        cursor.execute(query)
        result = cursor.fetchall()
    
    # Always commit after running SQL query so the changes are saved
    connection.commit()

    return result


def get_foods(food_name):
    with connection.cursor() as cursor:
        query = "SELECT * FROM (BrandedFood NATURAL JOIN Food) WHERE description LIKE %s;"
        cursor.execute(query, '%' + food_name + '%')
        result = cursor.fetchall()
    return result

def get_food(id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM (BrandedFood NATURAL JOIN Food) WHERE fdc_id = %s;"
        cursor.execute(query, id)
        result = cursor.fetchall()

    if len(result) != 0:
        return result[0]
    else:
        return {}

def get_nutrients(id):
    with connection.cursor() as cursor:
        query = "SELECT protein, fat, carb FROM FoodNutrient WHERE fdc_id = %s;"
        cursor.execute(query, id)
        result = cursor.fetchall()
    
    if len(result) != 0:
        return result[0]
    else:
        return {}

# store to EmotionEntry
def storeEmotionEntry(user_id, date, comment, emotion):

    with connection.cursor() as cursor:
        query = "insert into EmotionEntry (user_id, entry_date, comments, mood) VALUES(%s, %s, %s, %s)"
        val = (user_id, date, comment, emotion)
        cursor.execute(query, val)
        # print("works")
        # yay inserts into emotion entry!!
        
    connection.commit()


# store to SleepEntry
def storeSleepEntry(user_id, date, comment, sleep):

    with connection.cursor() as cursor:
        query = "insert into SleepEntry (user_id, entry_date, comments, duration) VALUES(%s, %s, %s, %s)"
        val = (user_id, date, comment, sleep)
        cursor.execute(query, val)
        # print("works")
        
    connection.commit()


# store to ExerciseEntry
def storeExerciseEntry(user_id, date, comment, intensity, duration, type):

    with connection.cursor() as cursor:
        query = "insert into ExerciseEntry (user_id, entry_date, comments, intensity, duration, type) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (user_id, date, comment, intensity, duration, type)
        cursor.execute(query, val)
        # print("works")
        
    connection.commit()


# store to FoodEntry
def storeFoodEntry(user_id, date, comment, calories, fat, carbs, protein, weight):

    with connection.cursor() as cursor:
        #storeFoodEntryNutrition(calories, fat, carbs, protein)
        
        query = "insert into FoodEntry (user_id, entry_date, comments, total_calories, total_fat, total_carbs, total_protein, weight) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, date, comment, calories, fat, carbs, protein, weight)
        cursor.execute(query, val)

        # print("works")
        
    connection.commit()

# Delete this eventually
def storeFoodEntryNutrition(calories, fat, carbs, protein):
    with connection.cursor() as cursor:
        query = "insert into FoodEntryNutrition (total_calories, total_fat, total_carbs, total_protein) VALUES(%s, %s, %s, %s)"
        val = (calories, fat, carbs, protein)
        cursor.execute(query, val)
        # print("works")
        
    connection.commit()

def getEmotionEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "SELECT * FROM EmotionEntry WHERE user_id = %s AND entry_date > (DATE(%s) - INTERVAL 7 DAY) AND entry_date < (DATE(%s) + INTERVAL 7 DAY);"
        val = (user_id, entry_date, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result

def getExerciseEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "SELECT * FROM ExerciseEntry WHERE user_id = %s AND entry_date > DATE(%s) - interval 7 day AND entry_date < (DATE(%s) + INTERVAL 7 DAY);"
        val = (user_id,entry_date, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result

def getSleepEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "SELECT * FROM SleepEntry WHERE user_id = %s AND entry_date > (DATE(%s) - INTERVAL 7 DAY) AND entry_date < (DATE(%s) + INTERVAL 7 DAY);"
        val = (user_id, entry_date, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result

def get_single_food_entry(user_id, entry_date):
   with connection.cursor() as cursor:
        query = "SELECT * FROM FoodEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result[0]  

def get_single_emotion_entry(user_id, entry_date):
   with connection.cursor() as cursor:
        query = "SELECT * FROM EmotionEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result[0]  

def get_single_exercise_entry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "SELECT * FROM ExerciseEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result[0]

def get_single_sleep_entry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "SELECT * FROM SleepEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result[0]


def getFoodEntry(user_id, entry_date):
   with connection.cursor() as cursor:
        query = "SELECT * FROM FoodEntry WHERE user_id = %s AND entry_date > (DATE(%s) - INTERVAL 7 DAY) AND entry_date < (DATE(%s) + INTERVAL 7 DAY);"
        val = (user_id, entry_date, entry_date)
        cursor.execute(query, val)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'string'
        else: 
            return result

def add_user(first_name, last_name, height, date_of_birth, email, password):
    with connection.cursor() as cursor:
        hashed_password = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        query = "insert into UserProfile (first_name, last_name, height, date_of_birth) " \
                "VALUES (%s, %s, %s, %s);"
        val = (first_name, last_name, height, date_of_birth)
        cursor.execute(query, val)

        query = "insert into UserProfileEmails (email, password) " \
                "VALUES (%s, %s);"
        val = (email, hashed_password)
        cursor.execute(query, val)

    connection.commit()
    return True

# updating form entries
 
def updateEmotionEntry(user_id, date, comment, emotion):
    with connection.cursor() as cursor:
        query = "UPDATE EmotionEntry SET comments = %s, mood = %s WHERE user_id = %s AND entry_date = %s;"
        val = (comment, emotion, user_id, date)
        cursor.execute(query, val)
    connection.commit()
 
def updateExerciseEntry(user_id, entry_date, comment, intensity, duration, type):
    with connection.cursor() as cursor:
        query = "UPDATE ExerciseEntry SET comments = %s, intensity = %s, duration = %s, type = %s WHERE user_id = %s AND entry_date = %s;"
        val = (comment, intensity, duration, type, user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def updateSleepEntry(user_id, entry_date, comment, sleep):
    with connection.cursor() as cursor:
        query = "UPDATE SleepEntry SET comments = %s, duration = %s WHERE user_id = %s AND entry_date = %s;"
        val = (comment, sleep, user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def updateFoodEntry(user_id, entry_date, comment, calories, fat, carbs, protein, weight):
    with connection.cursor() as cursor:
        #storeFoodEntryNutrition(calories, fat, carbs, protein) # just add the entry to foodentrynutrition
        query = "UPDATE FoodEntry SET comments = %s, total_calories = %s, total_fat = %s, total_carbs = %s, total_protein = %s, weight = %s WHERE user_id = %s AND entry_date = %s;"
        val = (comment, calories, fat, carbs, protein, weight, user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
###### do we want to update this? i guess we do, but how? what goes in "where" ?
#def updateFoodNutrition(calories, fat, carbs, protein):
#    with connection.cursor() as cursor:
#        query = "UPDATE FoodEntryNutrition SET total_calories = %s, total_fat = %s, total_carbs = %s, total_protein = %s WHERE ;"
#        val = (calories, fat, carbs, protein)
#        cursor.execute(query, val)
 
 
# deleting from db
def deleteEmotionEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "DELETE FROM EmotionEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def deleteExerciseEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "DELETE FROM ExerciseEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def deleteSleepEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        query = "DELETE FROM SleepEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def deleteFoodEntry(user_id, entry_date):
    with connection.cursor() as cursor:
        #deleteFoodNutrition(calories, fat, carbs, protein)
        query = "DELETE FROM FoodEntry WHERE user_id = %s AND entry_date = %s;"
        val = (user_id, entry_date)
        cursor.execute(query, val)
    connection.commit()
 
def deleteFoodNutrition(calories, fat, carbs, protein):
    with connection.cursor() as cursor:
        query = "DELETE FROM FoodEntryNutrition WHERE total_calories = %s AND total_fat = %s AND total_carbs = %s AND total_protein = %s;"
        val = (calories, fat, carbs, protein)
        cursor.execute(query, val)
    connection.commit()
        
def get_user(user_id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM UserProfile WHERE user_id=%s;"
        val = user_id
        cursor.execute(query, val)
        result = cursor.fetchall()

    connection.commit()
    return result[0]["first_name"], result[0]["last_name"], result[0]["height"], result[0]["date_of_birth"] # 0 index to access the first element of the result list

