import requests
import getpass
import tkinter as tk
from tkinter import filedialog

# Use Auth API
def get_request1():
    request1_type = {'1': 'Register:', '2': 'Login:', '3': 'Delete User:', '4': 'Change Password:', '5': 'Exiting application.'}
    print('\n\t1  Register\n\t2  Login\n\t3  Delete User\n\t4  Change Password\n\t5  Exit Application')
    while True:
        try:
            request1 = input(': ')
            if request1 not in ['1', '2', '3', '4', '5']:
                raise ValueError('Please choose 1, 2, 3, 4, or 5')
            
            print(request1_type[request1])
            if request1 == '5': # Exit app
                return request1, '', ''
            username = input('Enter username: ')
            password = getpass.getpass('Enter password: ')
            if request1 == '1': # Confirm password
                confirm_password = getpass.getpass('Enter password again: ')
                if (password != confirm_password):
                    print('ERROR: Passwords do not match')
                    return request1, username, ''
            new_password = ''
            if request1 == '4':
                new_password = getpass.getpass('New password: ')
                if (password == new_password):
                    print('ERROR: Pick a different password')
                    return request1, username, ''
            data = {'username': username, 'hashed_password': password}
            data_new_pass = {'username': username, 'hashed_password': new_password}
            if request1 == '1':
                response = register(data)
            elif request1 == '2':
                response = login(data)
            elif request1 == '3':
                response = delete(data)
            elif request1 == '4':
                response = login(data)
                if response != 'error':
                    response = change_pass(data_new_pass)
            return request1, username, response
        except ValueError as e:
            print(e)

# Use File Upload API
def get_request2(username):
    request2_type = {'1': 'Upload File:', '2': 'List Files:', '3': 'Remove File:', '4': 'Logout successful.'}
    print('\n\t1  Upload File\n\t2  List Files\n\t3  Remove File\n\t4  Logout')
    while True:
        try:
            request2 = input(': ')
            if request2 not in ['1','2','3','4']:
                raise ValueError('Please choose 1, 2, 3, or 4')
            
            print(request2_type[request2])
            if request2 == '4':
                return request2, ''
            if request2 == '1':
                print('Choose a file from the file explorer. You might have to go through the open windows on your device to find it.')
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()

                if file_path:
                    with open(file_path, 'rb') as file:
                        files = {'file': file}
                        response = file_upload(files, username)
            elif request2 == '2':
                data = {'username': username}
                response = list_files(data)
            elif request2 == '3':
                file_title = input('Which file would you like to remove?  ')
                data = {'username': username, 'file_title': file_title}
                response = remove_file(data)
            return request2, response
        except ValueError as e:
            print(e)

# AUTH FUNCTIONS
def register(data):
    response = requests.post('http://localhost:5000/registration', json=data)
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
        print('Registration failed. No response data.')
        return 'error'

def login(data):
    response = requests.post('http://localhost:5000/login', json=data)
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
        print('Login failed. No response data.')
        return 'error'

def delete(data):
    response = requests.post('http://localhost:5000/delete_user', json=data)
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
    response = requests.post('http://localhost:5000/change_password', json=data)
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
        response = requests.post(f'http://localhost:5000/upload_file/{username}', files=file)
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
        response = requests.post('http://localhost:5000/list_files', json=data)
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
        response = requests.post('http://localhost:5000/remove_file', json=data)
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

# START TEST
if __name__ == '__main__':
    print('\nWelcome to Lukas\' Smart Document Analyzer!\n')
    print('How would you like to start?')
    
    while True:
        request1, username, response = get_request1()
        if request1 == '2' and response == 'success':
            print('\nHello {}! What would you like to do today?'.format(username))
            while True:
                request2, response = get_request2(username)
                if request2 == '4':
                    break
        elif request1 == '5':
            break
    