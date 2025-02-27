import sqlite3

DATABASE = 'expense.db'

# Add a user to the database
def add_user(username, email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    """

    cursor.execute(insert_query, (username, email, password))
    conn.commit()
    cursor.close()
    conn.close()

# Fetch all users from the databse
def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    select_query = """
    SELECT user_id, username, email
    FROM users
    """
    cursor.execute(select_query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
