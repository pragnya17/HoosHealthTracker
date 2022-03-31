import pymysql.cursors
from db_secrets import secrets
import hashlib

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
    return result[0]

def get_nutrients(id):
    with connection.cursor() as cursor:
        query = "SELECT protein, fat, carb FROM FoodNutrient WHERE fdc_id = %s;"
        cursor.execute(query, id)
        result = cursor.fetchall()
    return result[0]

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
        storeFoodEntryNutrition(calories, fat, carbs, protein)
        
        query = "insert into FoodEntry (user_id, entry_date, comments, total_calories, total_fat, total_carbs, total_protein, weight) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, date, comment, calories, fat, carbs, protein, weight)
        cursor.execute(query, val)

        # print("works")
        
    connection.commit()


def storeFoodEntryNutrition(calories, fat, carbs, protein):
    with connection.cursor() as cursor:
        query = "insert into FoodEntryNutrition (total_calories, total_fat, total_carbs, total_protein) VALUES(%s, %s, %s, %s)"
        val = (calories, fat, carbs, protein)
        cursor.execute(query, val)
        # print("works")
        
    connection.commit()


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


def get_user(user_id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM UserProfile WHERE user_id=%s;"
        val = user_id
        cursor.execute(query, val)
        result = cursor.fetchall()

    connection.commit()
    return result[0]["first_name"], result[0]["last_name"], result[0]["height"], result[0]["date_of_birth"] # 0 index to access the first element of the result list

