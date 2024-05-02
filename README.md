# Smart Document Analyzer (mainly cloud)

### **Mission:** Analyze Catalog Search summarize Topics

## Table of Contents

- [Overview](#overview)
- [Functionality](#functionality)
- [APIs](#api)
- [Database](#database)
- [Updates](#updates)
- [Resources](#resources)

## Overview

This application provides a secure platform for users to upload various types of documents, and get various forms of information about the text. This includes changing your document to text.

Click [this link](#https://lchin10.github.io/chin-ec530-project2/) to visit the web application.

## Functionality

  - `Login` to a secure service to upload content
  - `Upload` documents
  - Can upload PDFs or images
  - Translate `documents to text`
  - Tag all documents with `keywords` and topics

*Not Implemented:*
  - I want the service to tag all my documents and paragraphs within every document with the keywords and know the topics each document cover
  - I should be able to access different paragraphs of different documents based on keywords
  - I should be able to to find all positive, neutral and negative paragraphs and sentences
  - Keywords within paragraphs should be searchable in government opendata, wikipedia and media organizations, e.g., NYTimes
  - I should find definition of keywords using open services (e.g., OpenAI)
  - I should be able to get summaries of each document
  - I want to discover content from the WEB to enhance story
  - I want to know all names, locations, institutions and address in my documents.
  - I want to upload different types of files (CSV, DOC, etc.)

## API

Runs one python script (*flask_run.py*) to run the Flask Application through Render

## API Modules

### Authorization and Authentication (auth_api.py):

- **Registration**
    - URL: `/registration`
    - Methods: `POST`
    - Data Params: `{username, password}`
- **User Info**
    - URL: `/user_info/<username>`
    - Methods: `GET`
    - Data Params: `{username, password}`
- **Login**
    - URL: `/login`
    - Methods: `POST`
    - Data Params: `{username, password}`
- **Delete User**
    - URL: `/delete_user`
    - Methods: `POST`
    - Data Params: `{username, password}`
- **Change Password**
    - URL: `/change_password`
    - Methods: `POST`
    - Data Params: `{username, new_password}`
- **Logout**
    - URL: `/logout`
    - Methods: `POST`
    - Data Params: `{username}`

### Secure File Uploader/Ingester (file_upload.py):
- **Upload File**
    - URL: `/upload_file/<username>`
    - Methods: `POST`
    - Data Params: `{file}`
- **Select File**
    - URL: `/select_file`
    - Methods: `POST`
    - Data Params: `{username, file_title}`
- **Remove File**
    - URL: `/remove_file`
    - Methods: `POST`
    - Data Params: `{username, file_title}`
- **List Files**
    - URL: `/list_files`
    - Methods: `POST`
    - Data Params: `{username}`

### Text NLP Analysis (text_nlp.py):
- **Get Metadata**
    - URL: `/get_metadata`
    - Methods: `POST`
    - Data Params: `{username, file_title}`
- **Doc To Text**
    - URL: `/doc_to_text`
    - Methods: `POST`
    - Data Params: `{username, file_title}`
- **Tag Keywords**
    - URL: `/tag_keywords_topics`
    - Methods: `POST`
    - Data Params: `{username, file_title}`

### Peer-To-Peer (p2p.py):
- **List Online Users**
    - URL: `/list_online_users`
    - Methods: `POST`
    - Data Params: `{}`
- **Send Message**
    - URL: `/send_message`
    - Methods: `POST`
    - Data Params: `{sender_username, recipient_username, message_text}`
- **Get Messages**
    - URL: `/get_messages`
    - Methods: `GET`
    - Data Params: `{sender_username, recipient_username}`

## Database

- **Users**
    - `U_ID [INTEGER PRIMARY KEY]`
    - `Username [TEXT]`
    - `Hashed_password [TEXT]`
    - `NOFiles [INTEGER]`
    - `Token [TEXT]`
- **Files**
    - `file_ID [INTEGER PRIMARY KEY]`
    - `file_title [TEXT]`
    - `file_data [BLOB]`
    - `U_ID [INTEGER FOREIGN KEY]`
- **FileInfo**
    - `file_ID [INTEGER FOREIGN KEY]`
    - `info_type [TEXT]`
    - `info [TEXT]`
- **P2P**
    - `MessageID [INTEGER PRIMARY KEY]`
    - `SenderID [INTEGER]`
    - `RecipientID [INTEGER]`
    - `MessageText [TEXT]`
    - `Timestamp [DATETIME]`

## Updates

### 4/29/2024:

- Updated unit testing script to work (test_script.py)

### 4/16/2024:

- Added functionality to get some file info:
    - Translation of doc to text (for PDF, using pypdf; for image, using pytesseract)
    - Tagging of doc with keywords/topics (using keybert)

### 4/7/2024:

- Added P2P Functionality:
    - List current online users
    - Chat feature with other online users

### 4/1/2024:

- Transitioned application from terminal to React Web Application
- Successfully called to web app APIs:
    - registration, login
    - uploading files, listing upser files, removing files
- Web app is set up on github pages (https://lchin10.github.io/chin-ec530-project2/)
- Database is set up with Render (https://chin-ec530-project2-2.onrender.com/ to call APIs in app)
    - Called flask application using gunicorn
    - Uses 4 workers as form of queue system

### 3/23/2024:

- Created working APIs for:
    - registration, login, deleting user, and changing password in module '*auth_api.py*'
    - uploading files, listing user files, and removing files in module '*file_upload.py*'
- Found a way to set up all APIs from multiple modules at once.
- Added logs and profiling for API calls
- Created database (database.db) using sqlite3
    - Created a script to reset and clear the existing database
- Created a client-side script to test API functionality
- Added unit testing of backend using python (test.py)

## Resources