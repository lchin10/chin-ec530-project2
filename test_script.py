import pytest
import requests
import os

baseUrl = ['https://chin-smart-document-analyzer.onrender.com', 'http://localhost:5000']
currUrl = baseUrl[0]


# AUTH FUNCTIONS
def register(data):
    response = requests.post(f'{currUrl}/registration', json=data)
    try:
            token = response.json().get('token')
            if token:
                print(token)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return f'ERROR: {error}'
    except requests.exceptions.JSONDecodeError:
        print('Registration failed. No response data.')
        return 'Registration failed. No response data.'

def login(data):
    response = requests.post(f'{currUrl}/login', json=data)
    try:
            token = response.json().get('token')
            if token:
                print(token)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return f'ERROR: {error}'
    except requests.exceptions.JSONDecodeError:
        print('Login failed. No response data.')
        return 'Login failed. No response data.'

def delete(data):
    response = requests.post(f'{currUrl}/delete_user', json=data)
    try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
    except requests.exceptions.JSONDecodeError:
        print('Delete User failed. No response data.')
        return 'error'

def change_pass(data):
    response = requests.post(f'{currUrl}/change_password', json=data)
    try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
    except requests.exceptions.JSONDecodeError:
        print('Change password failed. No response data.')
        return 'error'

def logout(data):
    response = requests.post(f'{currUrl}/logout', json=data)
    try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
    except requests.exceptions.JSONDecodeError:
        print('Change password failed. No response data.')
        return 'error'

# FILE FUNCTIONS
def file_upload(file, username):
        response = requests.post(f'{currUrl}/upload_file/{username}', files={'file': file})
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('File upload failed. No response data.')
            return 'error'

def list_files(data):
        response = requests.post(f'{currUrl}/list_files', json=data)
        try:
            message = response.json().get('message')
            if message:
                filenames = response.json().get('filenames')
                for i in range(len(filenames)):
                    print(f'\t{i+1}  {filenames[i]}')
                print(message)
                if filenames == []:
                    print('You have no files in your account.')
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('File listing failed. No response data.')
            return 'error'

def remove_file(data):
        response = requests.post(f'{currUrl}/remove_file', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('File remove failed. No response data.')
            return 'error'
        
# TEXT FUNCTIONS
def get_metadata(data):
        response = requests.post(f'{currUrl}/get_metadata', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('Doc to text failed. No response data.')
            return 'error'
        
def doc_to_text(data):
        response = requests.post(f'{currUrl}/doc_to_text', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('Doc to text failed. No response data.')
            return 'error'

def tag_keywords_topics(data):
        response = requests.post(f'{currUrl}/tag_keywords_topics', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('Tagging keywords failed. No response data.')
            return 'error'

def get_entities(data):
        response = requests.post(f'{currUrl}/get_entities', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('Getting file info failed. No response data.')
            return 'error'

def get_file_info(data):
        response = requests.post(f'{currUrl}/get_file_info', json=data)
        try:
            message = response.json().get('message')
            if message:
                print(message)
                return 'success'
            else:
                error = response.json().get('error')
                print(f'ERROR: {error}')
                return 'error'
        except requests.exceptions.JSONDecodeError:
            print('Getting file info failed. No response data.')
            return 'error'


# START TEST
def test_main():
    print('\nWelcome to Lukas\' Smart Document Analyzer!\n')

    
    # Register
    username = 'lukas'
    password = 'pass123'
    print(f'Registering as \'{username}\':')
    data = {'username': username, 'password': password}
    register_message = register(data)
    if register_message != 'success':
        print(f'Could not register. Deleting \'{username}\' and reregistering:')
        assert delete(data) == 'success'
        assert register(data) == 'success'

    # Upload Files
    filename = 'test_pdf_file.pdf'
    file_path = os.path.join(os.path.dirname(__file__), filename)
    print(f'Uploading file \'{filename}\':')
    with open(file_path, 'rb') as test_file:
        assert file_upload(test_file, username) == 'success'

    # List Files
    print(f'Listing files for \'{username}\':')
    data = {'username': username}
    assert list_files(data) == 'success'

    # Grab metadata
    print(f'Grabbing metadata:')
    data = {'username': username,'filename': filename}
    assert get_metadata(data) == 'success'

    # Doc to text
    print(f'Converting doc to text:')
    data = {'username': username,'filename': filename}
    assert doc_to_text(data) == 'success'

    # Tag keywords
    # print(f'Tagging doc with keywords:')
    # data = {'username': username,'filename': filename}
    # assert tag_keywords_topics(data) == 'success'

    # # Get entities (names, locations, institutions and address)
    # print(f'Getting entities (names, locations, institutions and address):')
    # data = {'username': username,'filename': filename}
    # assert get_entities(data) == 'success'

    # Get file info
    print(f'Getting file info:')
    data = {'username': username,'filename': filename}
    assert get_file_info(data) == 'success'

    # Logout
    print(f'Logging \'{username}\' out:')
    data = {'username': username}
    assert logout(data) == 'success'

    # Login
    print(f'Logging \'{username}\' back in:')
    data = {'username': username, 'password': password}
    assert login(data) == 'success'

    # Delete User
    print(f'Deleting user \'{username}\':')
    data = {'username': username, 'password': password}
    assert delete(data) == 'success'