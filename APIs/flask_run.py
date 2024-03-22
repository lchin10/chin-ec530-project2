from flask import Flask
from auth_api import auth_api_app
from file_upload import file_upload_app

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../Uploads'

# Register blueprints
app.register_blueprint(auth_api_app)
app.register_blueprint(file_upload_app)

if __name__ == '__main__':
    app.run(debug=True)
