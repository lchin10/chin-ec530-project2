"""
auth_api.py: Authorization and Authentication API

"""
from flask import Flask, request, jsonify
from flask import Blueprint
import sqlite3
import tracemalloc
import cProfile
import logging

# Logging
logging.basicConfig(filename='../Logs/auth_api.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Profiling
profile_folder = '../Profiling/'
profile = cProfile.Profile()

# Create Flask auth_api_app
auth_api_app = Blueprint('auth_api_app', __name__)

def get_db_connection():
    conn = sqlite3.connect('../Database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# User registration (generates token, add to database)
@auth_api_app.route('/registration', methods=['POST'])
def registration():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Registration initiated.')

    data = request.json
    username = data.get('username')
    hashed_password = data.get('hashed_password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if user exists
        cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 401
        
        cursor.execute('''
            INSERT INTO Users (Username, Hashed_password, NOFiles)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, 0))
        conn.commit()

        logger.info("Registration complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}registration.prof')
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        logger.info("Registration could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}registration.prof')
        return jsonify({'error': 'Username already exists'}), 401
    finally:
        conn.close()

# User info (retreive info from database)
@auth_api_app.route('/user_info/<username>', methods=['GET'])
def user_info(username):
    # Trace, profiling, logging
    profile.enable()
    logging.info('User Info initiated.')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    if user:
        logger.info("User Info complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}user_info.prof')
        return jsonify(dict(user)), 200
    else:
        logger.info("User Info could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}user_info.prof')
        return jsonify({'error': 'User not found'}), 404
    
# User login
@auth_api_app.route('/login', methods=['POST'])
def login():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Login initiated.')

    data = request.json
    username = data.get('username')
    hashed_password = data.get('hashed_password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Users
        WHERE Username = ? AND Hashed_password = ?
    ''', (username, hashed_password))

    user = cursor.fetchone()
    conn.close()

    if user:
        logger.info("Login complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}login.prof')
        return jsonify({'message': 'Login successful'}), 200
    else:
        logger.info("Login could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}login.prof')
        return jsonify({'error': 'Invalid credentials'}), 401

# Delete account
@auth_api_app.route('/delete_user', methods=['POST'])
def delete_user():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Delete user initiated.')

    data = request.json
    username = data.get('username')
    hashed_password = data.get('hashed_password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            DELETE FROM Users
            WHERE Username = ? AND Hashed_password = ?
        ''', (username, hashed_password))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'User does not exist or invalid credentials'}), 404
        
        logger.info("Delete complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}delete.prof')
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        logger.info("Delete could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}delete.prof')
        return jsonify({'error': str(e)}), 401
    finally:
        conn.close()

    
# Update user information
@auth_api_app.route('/update_user', methods=['POST'])
def update_user():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Update User initiated.')
    
# APP RUN
if __name__ == '__main__':
    auth_api_app.run(debug=True)