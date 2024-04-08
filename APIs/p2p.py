"""
file_upload.py: Secure File Uploader API

"""
from flask import Flask, request, jsonify
from flask import Blueprint, current_app
import os
import sqlite3
# import tracemalloc
import cProfile
import logging

# Logging
logging.basicConfig(filename='../Logs/flie_upload.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Profiling
profile_folder = '../Profiling/'
profile = cProfile.Profile()

p2p_app = Blueprint('p2p_app', __name__)

def get_db_connection():
    conn = sqlite3.connect('../Database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Define the route to list online users
@p2p_app.route('/list_online_users')
def list_online_users():

    # Trace, profiling, logging
    profile.enable()
    logging.info('Listing online users initiated.')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query the Users table for online users (non-empty token)
        cursor.execute("SELECT Username FROM Users WHERE Token != ''")
        online_users = [row[0] for row in cursor.fetchall()]

        logger.info("Listing online users complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}list_online_users.prof')
        return jsonify({'online_users': online_users}), 201
    except sqlite3.IntegrityError:
        logger.info("Cannot list online users.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}list_online_users.prof')
        return jsonify({'error': 'Cannot list online users'}), 401
    finally:
        conn.close()