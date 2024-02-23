"""
file_upload.py: Secure File Uploader API

"""
import sys

database = []
curr_file_id = ""
file_types = ["txt", "pdf", "png", "jpg"]

# File class
class File:
    def __init__(self, file_id, file_name, file_length, file_height, file_type):
        self.file_id = file_id
        self.file_name = file_name
        self.file_length = file_length
        self.file_height = file_height
        self.file_type = file_type

# Upload file
def upload_file(file, file_types):
    if (verify_file(file, file_types)):
        curr_file = file
        print('File successfully uploaded')

# Parse file
def parse_file(file):
    if (curr_file_id == ""):
        print('This is an error message', file=sys.stderr)

    # Call API for parsing file & getting metadata
    length, width = file.len, file.width
    file_type = file.type

    return file

# File handler (for different types of files)

# Image to text (using a ML model)
def image_to_text(file):
    text = ""
    # Call API for image -> text
    database.File_text = text
    return text

# Verify file (make sure it is a certain type/size)
def verify_file(file, file_types):
    parsed_file = parse_file(file)
    if (parsed_file.type not in file_types):
        print('File type is not supported', file=sys.stderr)

# Save file (after files are successfully ingested)
