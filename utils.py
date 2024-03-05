import mongo_connection

def create_new_user(username,password):
    client = mongo_connection.connect_to_mongo()
    if not client:
        print('Could not connect to MongoDB')
        return False
    
    db = client["STUPY_users"]

    collection = db["users"]
    user = {
        "username":username,
        "password":password
    }
    if collection.find_one({"username":username}):
        return False
    
    upload = collection.insert_one(user)

    return upload.inserted_id

def get_user(username,password):
    
    client = mongo_connection.connect_to_mongo()
    if not client:
        print('Could not connect to MongoDB')
        return False
    
    db = client["STUPY_users"]
    collection = db["users"]

    user = collection.find_one({"username":username})
    
    if password == user["password"]:
        return True
    else:
        return False

    