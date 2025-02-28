import sys
from db_operations import (
    add_user,
    authenticate_user,
    get_all_users,
    add_expense,
    get_user_expenses,
    update_expense,
    delete_expense
)

current_user_id = None

def welcome_menu():
    print("\n========== EXPENSE TRACKER CLI ==========")
    print("1. Login")
    print("2. Create a new user")
    print("3. Exit")

def create_new_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        add_user(username, email, password)
        print(f"User '{username}' created successfully!")
    except Exception as e:
        # Typically an IntegrityError if email is already in use
        print("Error creating user:", e)
        return False

def login():
    """
    Prompt user for email, password, then authenticate the user.
    If successful, sets current_user_id. Otherwise, prints error.
    """
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user_id = authenticate_user(email, password)
    if user_id:
        current_user_id = user_id
        print("Login successful!")
        return True
    else:
        print("Invalid email or password")
        return False
"""   
def handle_welcome_choice(choice):
    
    Takes the user's choice from the welcome menu and processes it.
    Returns:
        - True if we successfully logged in and should proceed to main menu
        - False otherwise (if we exit or remain in welcome menu)
    global current_user_id

    if choice == '1':       # Login
        login()
    elif choice == '2':     # Create new user
        create_new_user()
    elif choice == '3':     # Exit the program
        print("Exiting the program...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        return False
"""

def handle_welcome_choice(choice):
    global current_user_id

    if choice == '1':  # login
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user_id = authenticate_user(email, password)
        if user_id:
            current_user_id = user_id
            print("Login successful!")
            return True  # <-- Means we are logged in, can leave welcome loop
        else:
            print("Invalid email or password")
            return False

    elif choice == '2':  # create user

        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        try:
            add_user(username, email, password)
            print(f"User '{username}' created successfully!")
        except Exception as e:
            # Typically an IntegrityError if email is already in use
            print("Error creating user:", e)
            return False
    elif choice == '3':  # exit
        print("Exiting the program.")
        sys.exit(0)

    else:
        print("Invalid choice. Try again.")
        return False

def show_main_menu():
    """
    Show the main menu (expense operations, logout).
    Return the user's choice.
    """
    print("\n========== MAIN MENU ==========")
    print("1. Add an expense")
    print("2. View my expenses")
    print("3. Update an expense")
    print("4. Delete an expense")
    print("5. Logout")
    print("6. Help (re-display menu)")
    print("7. Quit")

def add_new_expense():
    """
    Prompt for expense details and insert into DB using current_user_id. 
    """
    global current_user_id
    if current_user_id is None:
        print("You must be logged in to add expenses")
        return
    try:
        category_id = int(input("Enter category ID: "))
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        description = input("Enter description (optional): ")
        add_expense(current_user_id, category_id, amount, date, description)
        #print("Expense added successfully!")
    except ValueError:
        print("Invalid input for user/category/amount. Please try again.")

def view_user_expenses():
    """
    Retrieve and display all expenses for the logged-in user.
    """
    global current_user_id
    if current_user_id is None:
        print("You must be logged in to view expenses")
        return
    expenses = get_user_expenses(current_user_id)
    if not expenses:
        print("No expenses found")
        return
    
    print(f"\nExpenses for user_id={current_user_id}: ")
    for (expense_id, user_id, cat_id, amt, dt, desc) in expenses:
        print(f"Expense ID: {expense_id}, Category ID: {cat_id}, "
              f"Ammount: {amt}, Date: {dt}, Description: {desc}")
        
def update_exiting_expense():
    """
    Prompt for expense ID, then ask which fields to update (amount, date, description).
    """
    global current_user_id
    if current_user_id is None:
        print("You must be logged in to update expenses.")
        return
    try:
        expense_id = int(input("Enter the expense ID to update: "))
        print("Leave a field blank if you do NOT want to update it.")

        new_amount_input = input("New amount (float): ")
        new_date_input = input("New date (YYYY-MM-DD): ")
        new_desc_input = input("New Description (optional): ")

        new_amount = float(new_amount_input) if new_amount_input.strip() else None
        new_date = new_date_input if new_date_input.strip() else None
        new_desc = new_desc_input if new_desc_input.strip() else None

        update_expense(expense_id, new_amount, new_date, new_desc)
        #print("Expense updated (if fields were provided).")
    except ValueError:
        print("Invalid input. Please ensure IDs and amounts are numeric")

def delete_existing_expense():
    """
    Prompt for expense ID and delete record.
    """
    global current_user_id
    if current_user_id is None:
        print("You must be logged in to delete an expense")
        return
    try:
        expense_id = int(input("Enter the expense ID to delete: "))
        delete_expense(expense_id)
        #print("Expense deleted successfully!")
    except ValueError:
        print("Invalid expense ID. Please enter a valid integer")

def handle_main_choice(choice):
    """
    Process a single command from the main menu.
    Retruns:
        - 'logout' if user chooses to log out
        - 'quit' if user wants to exit the program
        - 'help' if user wants to see menu again
        - None otherwise (continue in main loop)
    """
    if choice == '1':
        add_new_expense()
    elif choice == '2':
        view_user_expenses()
    elif choice == '3':
        update_exiting_expense()
    elif choice == '4':
        delete_existing_expense()
    elif choice == '5':
        # Logout
        print("Logging out...")
        return 'logout'
    elif choice == '6':
        # Help - show menu again
        return 'help'
    elif choice == '7':
        print("Exiting program...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
    return None

def main():
    global current_user_id

    # Phase 1: Welcome/ Authentication loop
    while True:
        welcome_menu()
        choice = input("Enter your choice: ")
        logged_in = handle_welcome_choice(choice)
        if logged_in:
            break       # proceed to main menu

    # Phase 2: Show main menu once after login
    show_main_menu()

    # Phase 3: Main loop that doesn't reprint the menu automatically
    while True:
        command = input("Enter a command number (or '6') for help: ").strip()
        result = handle_main_choice(command)
        if result == 'logout':
            current_user_id  = None
            # Return to the welcome menu loop
            return main()
        elif result == 'help':
            show_main_menu()
        # Otherwise, we keep looping

if __name__ == "__main__":
    main()

    