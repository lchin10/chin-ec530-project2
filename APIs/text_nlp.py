"""
text_nlp.py: Text NLP Analysis API

Use Text NLP Analysis API Calls. One possibility is SpaCy.

"""
from flask import Flask, request, jsonify
from flask import Blueprint, current_app
import os
import sqlite3
import cProfile
import logging
from pypdf import PdfReader

# Logging
logging.basicConfig(filename='../Logs/text_nlp.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Profiling
profile_folder = '../Profiling/'
profile = cProfile.Profile()

text_nlp_app = Blueprint('text_nlp_app', __name__)

file_types = {'txt', 'pdf', 'png', 'jpg'}

def get_db_connection():
    conn = sqlite3.connect('../Database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Translate doc to text
@text_nlp_app.route('/doc_to_text', methods=['POST'])
def doc_to_text():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Doc to text initiated.')
    
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
        u_id = user[0]

        # Check if file exists for user in file database
        cursor.execute('SELECT file_ID FROM Files WHERE file_title = ? AND U_ID = ?', (file_title, u_id))
        existing_file = cursor.fetchone()
        if not existing_file:
            return jsonify({'error': 'File not found'}), 404
        file_id = existing_file[0]

        # Determine file path and type
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_folder = os.path.join(upload_folder, username)
        file_path = os.path.join(user_folder, file_title)
        file_type = file_title.split('.')[-1]  # Extract file type from file title

        # Convert file to text based on its type
        if file_type == 'txt':
            with open(file_path, 'r') as f:
                text = f.read()
        elif file_type == 'pdf':
            pdf_reader = PdfReader(file_path)
            page = pdf_reader.pages[0]
            text = page.extract_text()
            pass
        elif file_type in ['png', 'jpg']:
            # Implement image to text conversion
            pass
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Check if the entry already exists in FileInfo
        cursor.execute('SELECT * FROM FileInfo WHERE file_ID = ? AND info_type = ?', (file_id, 'text'))
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({'error': 'Text already exists for this file'}), 400

        # Insert text into database
        cursor.execute('INSERT INTO FileInfo (info_type, info, file_ID) VALUES (?, ?, ?)', ('text', text, file_id))
        conn.commit()

        logger.info("Doc to text complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}doc_to_text.prof')
        return jsonify({'message': 'Doc to text successful'}), 200
    except sqlite3.IntegrityError:
        logger.info("Could not get text from doc.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}doc_to_text.prof')
        return jsonify({'error': 'Internal server error'}), 401
    finally:
        conn.close()

# # Find topics and keywords (for whole text and seperate paragraphs)
# def find_topics(file_ID):

# def find_keywords(file_ID):

# # Negative/positive parser (for sentences and paragraphs)
# def sentiment_parser(file_ID):

# # Text summarization
# def summarization(file_ID):

# # Name recognizer (names, locations, institutions and address)
# def name_recognizer(file_ID):

# APP RUN
if __name__ == '__main__':
    text_nlp_app.run(debug=True)
