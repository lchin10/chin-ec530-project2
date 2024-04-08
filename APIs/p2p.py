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