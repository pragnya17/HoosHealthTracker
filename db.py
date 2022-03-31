import pymysql.cursors
from db_secrets import secrets

# Connect to the database
connection = pymysql.connect(host= secrets['host'],
                             user= secrets['user'],
                             password= secrets['password'],
                             database= secrets['database'],
                             cursorclass=pymysql.cursors.DictCursor)

def get_users():
    """
    Example function for querying data.
    """

    with connection.cursor() as cursor:

        # Write query and execute it
        query = "SELECT * FROM UserProfile;"
        cursor.execute(query)

        # Retrieve all rows from query 
        # See https://pymysql.readthedocs.io/en/latest/modules/cursors.html for other fetch options
        # Note - fetchAll will return results as a dictionary
        # To read dictionary output easier, I recommend using https://beautifier.io/
        result = cursor.fetchall()
    
    # Always commit after running SQL query so the changes are saved
    connection.commit()

    return result

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
        storeFoodEntryNutrition(fat, carbs, protein, calories)
        
        query = "insert into FoodEntry (user_id, entry_date, comments, total_calories, total_fat, total_carbs, total_protein, weight) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, date, comment, calories, fat, carbs, protein, weight)
        cursor.execute(query, val)

        # print("works")
        
    connection.commit()

def storeFoodEntryNutrition(fat, carbs, protein, calories):
    with connection.cursor() as cursor:
        query = "insert into FoodEntryNutrition (total_fat, total_carbs, total_protein, calories) VALUES(%s, %s, %s, %s)"
        val = (fat, carbs, protein, calories)
        cursor.execute(query, val)
        # print("works")
        
    connection.commit()