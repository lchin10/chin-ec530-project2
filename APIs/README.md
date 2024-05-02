## API Calling:

***flask_run.py***:
    I created every API module as a blueprint Flask app rather than an actual Flask app. This allows for one Flask app in *flask_run.py* to register all the blueprints required and run all the modules at once.
    
## API Modules:

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