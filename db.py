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
