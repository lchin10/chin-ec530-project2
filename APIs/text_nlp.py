"""
text_nlp.py: Text NLP Analysis API

Use Text NLP Analysis API Calls. One possibility is SpaCy.

"""
import sys

database = []

# Find topics and keywords (for whole text and seperate paragraphs)
def find_topics(file_ID):
    if (not file_ID):
        print('Invalid file.', file=sys.stderr)
    else:
        file_text = database.File_text
        topics = []
        # Call API to get topics
        # topics.append(get_topics(file_text))
        return topics

def find_keywords(file_ID):
    if (not file_ID):
        print('Invalid file.', file=sys.stderr)
    else:
        file_text = database.File_text
        keywords = []
        # Call API to get keywords
        # keywords.append(get_keywords(file_text))
        return keywords

# Negative/positive parser (for sentences and paragraphs)
def sentiment_parser(file_ID):
    if (not file_ID):
        print('Invalid file.', file=sys.stderr)
    else:
        file_text = database.File_text
        sentient = []
        # Call API to get sentient
        # sentient.append(get_sentient(file_text))
        return sentient

# Text summarization
def summarization(file_ID):
    if (not file_ID):
        print('Invalid file.', file=sys.stderr)
    else:
        file_text = database.File_text
        summary = ""
        # Call API to get summary
        # summary = get_summary(file_text)
        return summary

# Name recognizer (names, locations, institutions and address)
def name_recognizer(file_ID):
    if (not file_ID):
        print('Invalid file.', file=sys.stderr)
    else:
        file_text = database.File_text
        names, locations, institutions, address = [],[],[],[]
        # Call API to get ..
        # names, locations, institutions, address = name_recognize(file_text)
        # database.names = names
        # database.locations = locations
        # database.institutions = institutions
        # database.address = address
        return names, locations, institutions, address
