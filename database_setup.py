import sqlite3

# Creates (or opens) a file-based database named expense.db
conn = sqlite3.connect('expense.db')
cursor = conn.cursor()

# Table Creation
create_user_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
"""

create_categories_table = """
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
);
"""

create_expense_table = """
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
"""

# Execute Table Creation
cursor.execute(create_user_table)
cursor.execute(create_categories_table)
cursor.execute(create_expense_table)

# Commit and Close
conn.commit()
conn.close()

print("Database and tables created successfully!")
