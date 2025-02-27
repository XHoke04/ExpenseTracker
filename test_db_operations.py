from db_operations import add_user, get_all_users

def test_add_and_get_users():
    # Add some users
    add_user("alice", "alice@example.com", "alicepass123")
    add_user("bob", "bob@example.com", "bobpass123")

    users = get_all_users()
    print("Users in DB: ", users)

if __name__ == "__main__":
    test_add_and_get_users()