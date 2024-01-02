import pymongo
from jsonschema import Draft202012Validator
from datetime import datetime
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
myschemas = mydb["schemas"]

def insert_schema(schema, name="NoName", description="NoDescription"):

    try:
        Draft202012Validator.check_schema(schema)
    except:
        return 0

    new_schema = {
        "name": name,
        "schema": schema,
        "description": description
    }

    myschemas.insert_one(new_schema)

    return 1

def get_schema(id="", name=""):
    if id == "" and name == "":
        return 0

    if id:
        return myschemas.find_one({"_id": ObjectId(id)})
    elif name:
        return myschemas.find_one({"name": name})

    return 0


def add_data(schema_id, data):
    schema_object = myschemas.find_one({"_id": ObjectId(schema_id)})
    schema = schema_object["schema"]
    name = schema_object["name"]
    if not schema:
        return 0

    draft_202012_validator = Draft202012Validator(schema)
    print(schema)
    print(data)
    if draft_202012_validator.is_valid(data):
        mycol = mydb[name]
        mycol.insert_one(data)
        return 1

    return 2


def get_data_of_schema(id="", name=""):
    if id == "" and name == "":
        return 0

    schema = None

    if id:
        schema = myschemas.find_one({"_id": ObjectId(id)})
    elif name:
        schema = myschemas.find_one({"name": name})

    if schema:
        schema_name = schema["name"]
        data = mydb[schema_name].find()
        return list(data)
    else:
        return 3


def get_all_schemas():
    all_schemas = []
    cursor = myschemas.find({})
    for schema in cursor:
        all_schemas.append(schema)
    return all_schemas

def drop_database():
    myclient.drop_database("mydatabase")  # for deleting a database before each run



