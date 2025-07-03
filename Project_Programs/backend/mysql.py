import mysql.connector
from mysql.connector import Error

# MySQL connection configuration
db_config = {
    'host': 'localhost',  # Replace with your MySQL host
    'user': 'root',  # Replace with your MySQL username
    'password': '1234',  # Replace with your MySQL password
    'database': 'virtualcamera'  # Replace with your MySQL database name
}

# Connect to the MySQL database
def connect_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Validate email and password
def validate(email, password): 
    if email and password:
        connection = connect_db()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return True
        return False
    return False

# Insert data into database
# Insert data into database
def insert(name, email, password, disability, role): 
    if name and not check(email) and password and disability and role:  # FIXED!
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, password, disability, role) 
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, disability, role))
            connection.commit()
            cursor.close()
            connection.close()
            return True  # Successfully inserted
    return False  # Failed (email exists or missing fields)


# Update data in database
def update(name, email, age):
    if not check(email):
        if name and email and age:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users SET name = %s, age = %s WHERE email = %s
                """, (name, age, email))
                connection.commit()
                cursor.close()
                connection.close()
                return True
    return False

# Check if email already exists
def check(email): 
    if not email:
        return False  # No email provided

    connection = connect_db()
    if not connection:
        print("Database connection failed!")
        return False  # Prevent signup if DB is down

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    data = cursor.fetchone()  # Fetch the first matching row

    cursor.close()
    connection.close()

    if data:
        print(f"Email {email} already exists in the database.")  
        return True  # Email already exists
    else:
        print(f"Email {email} is not found. Proceed with signup.")  
        return False  # Email does not exist, so allow signup



# Show all data in the database
def show(email): 
    if email:
        connection = connect_db()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            return data
    return False
