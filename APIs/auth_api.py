"""
auth_api.py: Authorization and Authentication API

"""
import sys

database = []

# User registration (generates token, add to database)
def registration(username, hash_password):
    if (username in database):
        print('Username already taken.', file=sys.stderr)
    else:
        return user_info(username, hash_password)

# User info (retreive info from database)
def user_info(username, hash_password):
    # Add info to DB
    user_ID = create_uid
    return user_ID

# User login
def login(username, hash_password):
    if (username not in database):
        print('Username does not exist.', file=sys.stderr)
    elif ([username, hash_password] not in database):
        print('Username or password is incorrect.', file=sys.stderr)
    else:
        user_ID = database.U_ID
        user_token = create_token(user_ID)
        # Add token to DB
        return user_token

# User logout
def logout(user_token):
    if (user_token not in database):
        print('Invalid token.', file=sys.stderr)
    else:
        remove_token_from_database(user_token)