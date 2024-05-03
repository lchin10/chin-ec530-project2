# Smart Document Analyzer (mainly cloud)

### **Mission:** Analyze Catalog Search summarize Topics

## Table of Contents

- [Overview](#overview)
- [Functionality](#functionality)
- [APIs](#api-modules)
- [Database](#database)
- [Full Functionality](#access-to-full-functionality)
- [Updates](#updates)
- [Resources](#resources)

## Overview

This application provides a secure platform for users to upload various types of documents, and get various forms of information about the text. This includes changing your document to text.

Click [this link](https://lchin10.github.io/smart-document-analyzer/) to visit the web application.

## Functionality

  - `Login` to a secure service to upload content
  - `Upload` documents
  - Can upload PDFs or images
  - Gets `metadata` of documents, including filename, type, size, width, height, time created, and time modified
  - Translate `documents to text`
  - Tag all documents with `keywords` and topics    ***not accesible through online web app*
  - Get `entities` of all names, locations, institutions and address in documents    ***not accesible through online web app*

*Not Implemented:*
  - I want the service to tag all my documents and paragraphs within every document with the keywords and know the topics each document cover
  - I should be able to access different paragraphs of different documents based on keywords
  - I should be able to to find all positive, neutral and negative paragraphs and sentences
  - Keywords within paragraphs should be searchable in government opendata, wikipedia and media organizations, e.g., NYTimes
  - I should find definition of keywords using open services (e.g., OpenAI)
  - I should be able to get summaries of each document
  - I want to discover content from the WEB to enhance story

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
- **Get Entities**
    - URL: `/get_entities`
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

## Access to Full Functionality

The Flask application for backend functionality is currently running on a free instance of Render, which has 512 MB and 0.1 CPU. Therefore, some features are not accessible through the web application deployed online through Github Pages. To have access to this functionality, you can go through the following steps:

1. Clone this repository to your computer/device.

        git clone https://github.com/lchin10/smart-document-analyzer.git

2. Download the required libraries/dependencies.

        pip install -r requirements.txt
        python -m spacy download en_core_web_sm

3. ****Important***: Navigate to '/src/App.js' and change line 19 to the following:

        const currUrl = baseUrl[1];

    This allows the web application to call API functionality from localhost rather than Render.

4. ****Optional***: If you want to start with a clean database, you can reinitiate the database.

        cd Database
        python database_init.py        

5. Run the Flask Application.

        cd APIs
        python flask_run.py

6. Open a new terminal, then run the web application.

        npm start

## Updates

### 5/3/2024:

- Added file functionality (text_nlp.py) for:
  - Getting metadata (using PdfReader)
  - Getting entities of documents (using SpaCy Model 'en_core_web_sm')

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
- Web app is set up on github pages (https://lchin10.github.io/smart-document-analyzer/)
- Database is set up with Render (https://chin-smart-document-analyzer.com/ to call APIs in app)
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

- [ReactJS Web Application](https://react.dev/)
- [Render Application Deployment](render.com)
- [SpaCy Language Model](https://spacy.io/usage/models)
- [KeyBERT](https://github.com/MaartenGr/KeyBERT)
