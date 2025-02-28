import sqlite3
import bcrypt

DATABASE = 'expense.db'

# Add a user to the database
def add_user(username, email, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    """

    cursor.execute(insert_query, (username, email, hashed))
    conn.commit()
    cursor.close()
    conn.close()

# Get user by email
def get_user_by_email(email):
    """
    Return a user's row given an email, or None if not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "SELECT user_id, username, email, password FROM users WHERE email = ?"
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row # (user_id, username, email, password) or None

# Authenticate a user with given email and password
def authenticate_user(email, password):
    """
    Check if there's a user with the given email and password.
    Return the user_id if valid, otherwise None.
    In a real app, we'd need to compare hashed passwords for security (possibly implement later)
    """
    user = get_user_by_email(email)
    if user:
        user_id, username, user_email, stored_hashed_pw = user
        # stored_hashed_pw is in bytes, password is in plaintext
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw):
            return user_id
        else:
            print("Error, invalid")
    return None

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

## Expense Table Operations

def add_expense(user_id, category_id, amount, date, description=None):
    """
    Insert a new expense record into the exepnses table.

    :param user_id: ID of the user associated with this expense
    :param category_id: ID of the category
    :param amount: Numeric value representing how much was spent
    :param date: String representing the date of the expense (e.g. '2025-01-05')
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    INSERT INTO expenses (user_id, category_id, amount, date, description)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (user_id, category_id, amount, date, description))

    conn.commit()
    cursor.close()
    conn.close()
    print("Expense added successfully")

def get_user_expenses(user_id):
    """
    Retrieve all expenses for a given user, most recent first.

    :param user_id: The user for whom to retrieve expenses
    :return: A list of tuples, each tuple representing one expense record
            (expense_id, user_id, category_id, amount, date, description)
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT expense_id, user_id, category_id, amount, date, description
    FROM expenses
    WHERE user_id = ?
    ORDER BY date DESC
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def update_expense(expense_id, new_amount=None, new_date=None, new_description=None):
    """
    Update an existing expense record. Only updates the fields that are provided. 

    :param expense_id: The ID of the expense to update
    :param new_amount: The new amount (optional)
    :param new_date: The new date (optional)
    :param new_description: The new description (optional)
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Build the update query dynamically based on which arguments are None
    update_parts = []
    params = []

    if new_amount is not None:
        update_parts.append("amount = ?")
        params.append(new_amount)
    if new_date is not None:
        update_parts.append("date = ?")
        params.append(new_date)
    if new_description is not None:
        update_parts.append("description = ?")
        params.append(new_description)

    # If no fields were provided, nothing to update
    if not update_parts:
        print("No fields to update.")
        conn.close()
        return
    
    update_clause = ", ".join(update_parts)
    query = f"UPDATE expenses SET {update_clause} WHERE expense_id = ?"
    params.append(expense_id)

    cursor.execute(query, tuple(params))
    conn.commit()

    if cursor.rowcount == 0:
        print(f"No expense found with ID {expense_id}, or no changes made")
    else:
        print("Expense updated successfully!")

    cursor.close()
    conn.close()

def delete_expense(expense_id):
    """
    Delete an expense recorded by its ID

    :param expense_id: The ID of the expense to delete
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = "DELETE FROM expenses WHERE expense_id = ?"
    cursor.execute(query, (expense_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        print(f"No expense found with ID {expense_id}.")
    else:
        print("Expense deleted successfully!")

    cursor.close()
    conn.close()