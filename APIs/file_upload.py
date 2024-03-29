"""
file_upload.py: Secure File Uploader API

"""
from flask import Flask, request, jsonify
from flask import Blueprint, current_app
import os
import sqlite3
import tracemalloc
import cProfile
import logging

# Logging
logging.basicConfig(filename='../Logs/flie_upload.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Profiling
profile_folder = '../Profiling/'
profile = cProfile.Profile()

file_upload_app = Blueprint('file_upload_app', __name__)
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = '../Uploads'

file_types = {'txt', 'pdf', 'png', 'jpg'}

def get_db_connection():
    conn = sqlite3.connect('../Database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in file_types

# Upload file
@file_upload_app.route('/upload_file/<username>', methods=['POST'])
def upload_file(username):
    # Trace, profiling, logging
    profile.enable()
    logging.info('Upload file initiated.')
    
    file = request.files['file']
    file_title = file.filename
    file_data = file.read()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 401
        
        # Check if file is valid
        if file_title == '':
            return jsonify({'error': 'No selected file'}), 401
        
        if not allowed_file(file_title):
            return jsonify({'error': 'Invalid file type. File type must be \'.txt\', \'.pdf\', \'.png\', or \'.jpg\''}), 401
        
        # Get UID from username
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        u_id = user['U_ID']

        # Check if file exists for user in file database
        cursor.execute('SELECT * FROM Files WHERE file_title = ? AND U_ID = ?', (file_title, u_id))
        existing_file = cursor.fetchone()
        if existing_file:
            return jsonify({'error': 'File title already exists for the user'}), 404
        
        cursor.execute('SELECT * FROM Files WHERE file_data = ? AND U_ID = ?', (file_data, u_id))
        existing_file = cursor.fetchone()
        if existing_file:
            return jsonify({'error': 'File data already exists for the user'}), 404
                
        # Add file to Uploads folder
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_folder = os.path.join(upload_folder, username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        file_path = os.path.join(user_folder, file_title)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Insert file into database
        cursor.execute('INSERT INTO Files (file_title, file_data, U_ID) VALUES (?, ?, ?)', (file_title, file_data, u_id))

        # Update NOFiles for user
        cursor.execute('UPDATE Users SET NOFiles = NOFiles + 1 WHERE U_ID = ?', (u_id,))
        
        conn.commit()

        logger.info("Upload complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}upload.prof')
        return jsonify({'message': 'File uploaded successfully'}), 201
    except sqlite3.IntegrityError:
        logger.info("Upload could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}upload.prof')
        return jsonify({'error': 'Username already exists'}), 401
    finally:
        conn.close()

# Parse file
@file_upload_app.route('/parse_file', methods=['POST'])
def parse_file():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Parse file initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('file_title')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # File not in db
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (username,))
    except sqlite3.IntegrityError:
        logger.info("Upload could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}upload.prof')
        return jsonify({'error': 'Username already exists'}), 401
    finally:
        conn.close()
    

# Select file
@file_upload_app.route('/select_file', methods=['POST'])
def select_file():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Select file initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('file_title')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get UID from username
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        u_id = user['U_ID']

        # Check if file exists for user in file database
        cursor.execute('SELECT * FROM Files WHERE file_title = ? AND U_ID = ?', (file_title, u_id))
        existing_file = cursor.fetchone()
        if not existing_file:
            return jsonify({'error': 'File not found'}), 404
    except sqlite3.IntegrityError:
        logger.info("Select could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}select.prof')
        return jsonify({'error': 'Internal server error'}), 401
    finally:
        conn.close()


# Remove file
@file_upload_app.route('/remove_file', methods=['POST'])
def remove_file():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Upload file initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('file_title')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get UID from username
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        u_id = user['U_ID']

        # Check if file exists for user in file database
        cursor.execute('SELECT * FROM Files WHERE file_title = ? AND U_ID = ?', (file_title, u_id))
        existing_file = cursor.fetchone()
        if not existing_file:
            return jsonify({'error': 'File not found'}), 404

        # Remove file from uploads folder
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_folder = os.path.join(upload_folder, username)
        file_path = os.path.join(user_folder, file_title)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Remove file from database
        cursor.execute('DELETE FROM Files WHERE file_title = ? AND U_ID = ?', (file_title, u_id))

        # Update NOFiles for user
        cursor.execute('UPDATE Users SET NOFiles = NOFiles - 1 WHERE U_ID = ?', (u_id,))

        conn.commit()

        logger.info("File removal complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}remove_file.prof')
        return jsonify({'message': 'File removed successfully'}), 200        
    except sqlite3.IntegrityError:
        logger.info("Remove could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}remove.prof')
        return jsonify({'error': 'Internal server error'}), 401
    finally:
        conn.close()

        
# List files (from db)
@file_upload_app.route('/list_files', methods=['POST'])
def list_files():
    # Trace, profiling, logging
    profile.enable()
    logging.info('List files initiated.')

    data = request.json
    username = data.get('username')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get UID from username
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        u_id = user['U_ID']

        # Get list of filenames for the user fropm database
        cursor.execute('SELECT file_title FROM Files WHERE U_ID = ?', (u_id,))
        files = cursor.fetchall()
        filenames = [file['file_title'] for file in files]

        logger.info("List files complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}list_files.prof')
        return jsonify({'message': 'Files listed successfully', 'filenames': filenames}), 200
    except Exception as e:
        logger.info("List could not be completed.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}list_files.prof')
        return jsonify({'error': 'Internal server error'}), 401
    
    file_list = [dict(file) for file in files]
    
    logger.info('Files retrieved successfully.')
    profile.disable()
    profile.dump_stats(f'{profile_folder}get_files.prof')
    
    return jsonify(file_list), 200

# APP RUN
if __name__ == '__main__':
    file_upload_app.run(debug=True)