from db import db
from models import UserType

def add_user_type(name):
    """
    Adds a new user type to the database.

    Args:
        name (str): The name of the user type.

    Returns:
        UserType: The created UserType object.
    """
    user_type = UserType(name=name)
    db.session.add(user_type)
    db.session.commit()
    return user_type
