"""
file_upload.py: Secure File Uploader API

"""
from flask import Flask, request, jsonify
from flask import Blueprint
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
@p2p_app.route('/list_online_users', methods=['POST'])
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


# Route to send a message
@p2p_app.route('/send_message', methods=['POST'])
def send_message():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Send message initiated.')

    data = request.json
    sender_username = data.get('sender_username')
    recipient_username = data.get('recipient_username')
    message_text = data.get('message_text')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get U_IDs
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (sender_username,))
        sender = cursor.fetchone()
        if not sender:
            return jsonify({'error': 'Sender not found'}), 404
        sender_id = sender['U_ID']
        
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (recipient_username,))
        recipient = cursor.fetchone()
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        recipient_id = recipient['U_ID']

        # Insert message into database
        cursor.execute('''
            INSERT INTO P2P (SenderID, RecipientID, MessageText)
            VALUES (?, ?, ?)
        ''', (sender_id, recipient_id, message_text))
        conn.commit()

        logger.info("Sending message complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}send_message.prof')
        return jsonify({'message': 'Message sent successfully'}), 200
    except sqlite3.IntegrityError:
        logger.info("Cannot send message.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}send_message.prof')
        return jsonify({'error': 'Cannot send message'}), 401
    finally:
        conn.close()

# Route to retrieve messages between two users
@p2p_app.route('/get_messages', methods=['GET'])
def get_messages():
    # Trace, profiling, logging
    profile.enable()
    logging.info('Get messages initiated.')

    sender_username = request.args.get('sender_username')
    recipient_username = request.args.get('recipient_username')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get U_IDs
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (sender_username,))
        sender = cursor.fetchone()
        if not sender:
            return jsonify({'error': 'Sender not found'}), 404
        sender_id = sender['U_ID']
        
        cursor.execute('SELECT U_ID FROM Users WHERE Username = ?', (recipient_username,))
        recipient = cursor.fetchone()
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        recipient_id = recipient['U_ID']

        # Retrieve messages from database
        cursor.execute('''
            SELECT * FROM P2P
            WHERE (SenderID = ? AND RecipientID = ?)
            OR (SenderID = ? AND RecipientID = ?)
            ORDER BY Timestamp
        ''', (sender_id, recipient_id, recipient_id, sender_id))
        messages = cursor.fetchall()
        logger.info("Getting messages complete.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}get_messages.prof')
        return jsonify({'messages': [dict(message) for message in messages]}), 200
    except sqlite3.IntegrityError:
        logger.info("Cannot get messages.")
        profile.disable()
        profile.dump_stats(f'{profile_folder}get_messages.prof')
        return jsonify({'error': 'Cannot get messages'}), 401
    finally:
        conn.close()

if __name__ == '__main__':
    p2p_app.run(debug=True)