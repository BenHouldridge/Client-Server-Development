from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = username
        PASS = password
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30323
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        #print(self.collection)
        #print(type(self.collection))

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if self.input_is_valid(data):
            try:
                self.database.animals.insert_one(data)  # data should be dictionary  
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
            

# Create method to implement the R in CRUD.
    def read(self, criteria):
        cursor = self.collection.find(criteria)
        return list(cursor)


    def input_is_valid(self, data):
        try:
            if data is None:
                raise Exception("Nothing to save, because data parameter is empty.")
            elif isinstance(data, dict) == False:
                raise Exception("Invalid input format. Expected JSON dictionary.")
            else:
                return True
        except Exception as e:
            print(e)
            
    def update(self, lookup_key, lookup_value, update_data):
        if self.input_is_valid(update_data):
            try:
                to_be_updated = self.read({lookup_key: lookup_value})
                query = {lookup_key: lookup_value}
                result = self.collection.update_many(query, {'$set': update_data})
                print('Documents found: ' + str(result.matched_count))
                print('Documents modified: ' + str(result.modified_count))
                return result.modified_count
            except Exception as e:
                print(e)
                return 0
        else:
            return 0
    
    def delete(self, criteria):
        result = self.collection.delete_many(criteria)
        print('Documents deleted: ' + str(result.deleted_count))
        return result.deleted_count
            
        