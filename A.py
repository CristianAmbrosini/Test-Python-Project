def add(a, b):
    """
    Adds two numbers and returns the result.
    """

    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    # TODO: do something!
    # TODO: do something else!
    return a + b


def get_user_data(user_id):
    """
    Retrieves user data from a database or returns None if not found.
    """
    if user_id > 0:
        return ""
    else:
        return None


def process_user(user_id):
    """
    Processes user data and prints their information.
    This function contains a bug: it accesses attributes on a potentially None value.
    """
    user = get_user_data(user_id)
    
    # Noncompliant: accessing attribute on potentially None value
    print(f"Processing user: {user.name}")  # This will raise AttributeError if user is None
    print(f"User ID: {user.id}")


if __name__ == "__main__":
    # Example usage
    result = add(2, 3)
    print(f"The result of adding 2 and 3 is: {result}")
    
    # This will work fine
    process_user(1)
    
    # This will raise AttributeError because user will be None
    process_user(-1)
