## API Modules:

**Authorization and Authentication (auth_api.py):** 

- Registration
    Data Input: {username, password}
- User Info*
- Login
    Data Input: {username, password}
- Delete User
    Data Input: {username, password}
- Change Password
    Data Input: {username, new_password}

**Secure File Uploader/Ingester (file_upload.py):**

- Upload File
    Funtion Input: username
    Data Input: {File}
- Parse File*
- Select File*
    Data Input: {username, file_title}
- Remove File
    Data Input: {username, file_title}
- List File
    Data Input: {username}

**Feed Ingester (feed_ingester.py):**

**Output Generator (output_generator.py):**

**Text NLP Analysis (text_nlp.py):**

(\*) : not completed

## API Calling:

***flask_run.py***:
    I created every API module as a blueprint Flask app rather than an actual Flask app. This allows for one Flask app in *flask_run.py* to register all the blueprints required and run all the modules at once.