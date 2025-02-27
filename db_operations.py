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

def get_user_expense(user_id):
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
        params.update(new_amount)
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
    cursor.close()
    conn.close()
    print("Expense updated successfully")

def delete_expense(expense_id):
    """
    Delete an expense recorded by its ID

    :param expense_id: The ID of the expense to delete
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    DELETE FROM expenses
    WHERE expense_id = ?
    """
    cursor.execute(query, (expense_id,))

    conn.commit()
    cursor.close()
    conn.close()
    print("Expense deleted successfully!")