import pymysql.cursors
from db_secrets import secrets
import hashlib

# Connect to the database
connection = pymysql.connect(host= secrets['host'],
                             user= secrets['username'],
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