"""
text_nlp.py: Text NLP Analysis API

Use Text NLP Analysis API Calls. One possibility is SpaCy.

"""
from flask import Flask, request, jsonify
from flask import Blueprint, current_app
import os
import datetime
import sqlite3
import cProfile
import logging
from pypdf import PdfReader
import pytesseract
from PIL import Image
import json
from keybert import KeyBERT
from pypdf import PdfReader

# Logging
logging.basicConfig(filename='../Logs/text_nlp.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Profiling
profile_folder = '../Profiling/'
profile = cProfile.Profile()

text_nlp_app = Blueprint('text_nlp_app', __name__)

def get_db_connection():
    conn = sqlite3.connect('../Database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get doc metadata (filename, type, size, width, height, time created, time modified)
@text_nlp_app.route('/get_metadata', methods=['POST'])
def get_metadata():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Grabbing metadata initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('filename')

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
            return jsonify({'error': f'File \'{file_title}\' not found'}), 404
        file_id = existing_file[0]

        # Determine file path and type
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_folder = os.path.join(upload_folder, username)
        file_path = os.path.join(user_folder, file_title)
        file_type = file_title.split('.')[-1]

        # Get metadata
        file_size = os.path.getsize(file_path)
        file_stat = os.stat(file_path)
        file_creation_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
        file_modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        width, height = None, None
        if file_type.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            with Image.open(file_path) as img:
                width, height = img.size
        elif file_type.lower() == 'pdf':
            with open(file_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                first_page = reader.pages[0] # First page
                width = first_page.mediabox.width/72.0
                height = first_page.mediabox.height/72.0
        metadata = {
            'filename': file_title,
            'type': file_type,
            'size (bytes)': file_size,
            'width (inches)': width,
            'height (inches)': height,
            'creation_time': file_creation_time.isoformat(),
            'modification_time': file_modification_time.isoformat()
        }
        metadata_json = json.dumps(metadata)

        # Check if the entry already exists in FileInfo
        cursor.execute('SELECT * FROM FileInfo WHERE file_ID = ? AND info_type = ?', (file_id, 'metadata'))
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({'error': 'Metadata already exists for this file'}), 400
        
        # Insert metadata into database
        cursor.execute('INSERT INTO FileInfo (info_type, info, file_ID) VALUES (?, ?, ?)', ('metadata', metadata_json, file_id))
        conn.commit()

        logger.info("Grabbing metadata complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}get_metadata.prof')
        return jsonify({'message': 'Grabbing metadata successful'}), 200
    except sqlite3.IntegrityError:
        logger.info("Could not get metadata.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}get_metadata.prof')
        return jsonify({'error': 'Internal server error'}), 401
    finally:
        conn.close()

# Translate doc to text
@text_nlp_app.route('/doc_to_text', methods=['POST'])
def doc_to_text():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Doc to text initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('filename')

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
            return jsonify({'error': f'File \'{file_title}\' not found'}), 404
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
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_type in ['png', 'jpg']:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
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

# Find topics and keywords (for whole text and seperate paragraphs)
@text_nlp_app.route('/tag_keywords_topics', methods=['POST'])
def tag_keywords_topics():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Tag keywords and topics initiated.')
    
    data = request.json
    username = data.get('username')
    file_title = data.get('filename')

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
            return jsonify({'error': f'File \'{file_title}\' not found'}), 404
        file_id = existing_file[0]

        # Check if text has been extracted
        cursor.execute('SELECT info FROM FileInfo WHERE file_ID = ? AND info_type = ?', (file_id, 'text'))
        text_info = cursor.fetchone()
        if not text_info:
            return jsonify({'error': 'Text information not found for this file'}), 400
        text = text_info['info']

        # Check if the entry already exists in FileInfo
        cursor.execute('SELECT * FROM FileInfo WHERE file_ID = ? AND info_type = ?', (file_id, 'keyword'))
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({'error': 'Keywords already exist for this file'}), 400
        
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None)

        # Serialize keywords into a JSON-like string
        keywords_json = json.dumps(keywords)

        # Insert keywords/topics into the database as a single JSON-like string
        cursor.execute('INSERT INTO FileInfo (info_type, info, file_ID) VALUES (?, ?, ?)', ('keyword', keywords_json, file_id))
        conn.commit()

        logger.info("Tag keywords and topics complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}tag_keywords_topics.prof')
        return jsonify({'message': 'Tag keywords and topics successful'}), 200
    except sqlite3.IntegrityError:
        logger.info("Could not tag keywords and topics.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}tag_keywords_topics.prof')
        return jsonify({'error': 'Internal server error'}), 401
    finally:
        conn.close()

# # Negative/positive parser (for sentences and paragraphs)
# def sentiment_parser(file_ID):

# # Text summarization
# def summarization(file_ID):

# # Name recognizer (names, locations, institutions and address)
# def name_recognizer(file_ID):

# APP RUN
if __name__ == '__main__':
    text_nlp_app.run(debug=True)
