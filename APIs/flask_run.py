"""
flask_run.py: Runs Flask Application in full

"""
from flask import Flask
from flask_cors import CORS
from auth_api import auth_api_app
from file_upload import file_upload_app
from p2p import p2p_app
from text_nlp import text_nlp_app

# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = '../Uploads'
app.config['SECRET_KEY'] = 'Tf&2L$nDp9@qBhV*WY3#Zc7u8Xe4@FmA'

# Register blueprints
app.register_blueprint(auth_api_app)
app.register_blueprint(file_upload_app)
app.register_blueprint(p2p_app)
app.register_blueprint(text_nlp_app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
