import mongo_connection

from datetime import datetime

def create_new_user(username,password):
    """
    Function to create a new user in the database. 
    It will return False if the user already exists, 
    and the id of the user if it is created.
    Requires username and password as strings.
    """

    # attempt to connect to the database
    client = mongo_connection.connect_to_mongo()

    if not client:

        print('Could not connect to MongoDB')

        return False
    
    # declare the database and the collection
    db = client["STUPY_users"]

    collection = db["users"]

    # create the dictionary with the user data
    user = {
        "username":username,
        "password":password
    }
    # check if the user already exists
    # if it does, return False
    if collection.find_one({"username":username}):

        return False
    
    # if the user does not exist, insert it into the database
    upload = collection.insert_one(user)

    # return the id of the user
    return upload.inserted_id


def get_user(username,password):
    """
    Functioni to find users in the database.
    It will return True if the user exists and the password is correct,
    and False if the user does not exist or the password is incorrect.
    Requires username and password as strings.
    """
    # connect to the database
    client = mongo_connection.connect_to_mongo()

    if not client:

        print('Could not connect to MongoDB')

        return False
    
    # declare the database and the collection
    db = client["STUPY_users"]

    collection = db["users"]

    # find the user in the database
    user = collection.find_one({"username":username})
    
    # only return the user if the password is correct
    # this is to avoid sending the password to the client

    if password == user["password"]:

        return True
    
    else:

        return False


def new_thread(title, content, username):
    """
    Function to create a new thread in the database.
    It will return the id of the thread if it is created.
    Requires title and content as strings, and username as a string.
    """
    # connect to the database
    client = mongo_connection.connect_to_mongo()

    if not client:

        print('Could not connect to MongoDB')

        return False
    
    # declare the database and the collection
    db = client["STUPY_users"]

    collection = db["threads"]

    # create the dictionary with the thread data
    thread = {
        "title":title,
        "content":content,
        "date_created":datetime.utcnow(),
        "author_id":username
    }

    # insert the thread into the database
    # it is still necessary some logic to prevent the user to create 
    # threads too quickly
    # but the code is not that fast so it is not a problem for now hehe
    upload = collection.insert_one(thread)

    return upload.inserted_id

def get_threads(length = 5):
    """
    Function to get the threads from the database.
    It will return a list of threads.
    Requires length as an integer.
    """
    # connect to the database
    client = mongo_connection.connect_to_mongo()

    if not client:

        print('Could not connect to MongoDB')

        return False
    
    # declare the database and the collection
    db = client["STUPY_users"]

    collection = db["threads"]

    # find the threads in the database
    # the length parameter is not used in app.py yet, but
    # it is for the future
    cursor = collection.find().sort([("date_created", -1)]).limit(length)

    # create the list of threads because the code above returns a cursor (olbject)
    threads = list(cursor)

    return threads
    
