import pymongo
from jsonschema import Draft202012Validator
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient.drop_database("mydatabase") #for deleting a database before each run
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
        return myschemas.find_one({"_id": id})

    return myschemas.find_one({"name": name})


def add_data(schema_id, data):
    schema_object = myschemas.find_one({"_id": schema_id})
    schema = schema_object["schema"]
    name = schema_object["name"]
    if schema is None:
        return 0

    draft_202012_validator = Draft202012Validator(schema)

    if draft_202012_validator.is_valid(data):
        mycol = mydb[name]
        mycol.insert_one(data)
        return 1

    return 0


def get_data_of_schema(id="", name=""):
    if id == "" and name == "":
        return 0

    if id:
        schema = myschemas.find_one({"_id": id})
    else:
        schema = myschemas.find_one({"name": name})

    if schema:
        schema_name = schema["name"]
        data = mydb[schema_name].find()
        return list(data)
    else:
        return 0


def get_all_schemas():
    all_schemas = []
    cursor = myschemas.find({})
    for schema in cursor:
        all_schemas.append(schema)
    return all_schemas

## Define test bench function
def test_bench():
    # Adding schemas with multiple fields of multiple data types
    schema1 = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "dob": {"type": "string", "format": "date"}
        }
    }

    schema2 = {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "salary": {"type": "number"},
            "start_date": {"type": "string", "format": "date"},
            "active": {"type": "boolean"}
        }
    }

    schema3 = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string", "format": "date"},
            "views": {"type": "integer"}
        }
    }

    # Adding multiple schemas multiple times
    for _ in range(3):
        insert_schema(schema1, name="Schema1", description="Schema with multiple fields of different data types")
        insert_schema(schema2, name="Schema2", description="Another schema with different field types")
        insert_schema(schema3, name="Schema3", description="Yet another schema with various fields")

        # Testing get_schema multiple times
        print(get_schema(name="Schema1"))
        schema_id = myschemas.find_one({"name": "Schema2"})["_id"]
        print(get_schema(id=schema_id))

        # Adding data multiple times for different schemas
        schema_id = myschemas.find_one({"name": "Schema1"})["_id"]
        data_string = {"name": "Alice"}
        print(add_data(schema_id, data_string))

        schema_id = myschemas.find_one({"name": "Schema2"})["_id"]
        data_integer = {"salary": 50000.00, "active": True}
        print(add_data(schema_id, data_integer))

        # Retrieving data of schemas multiple times
        print(get_data_of_schema(name="Schema1"))
        print(get_data_of_schema(name="Schema2"))

        # Retrieving all schemas multiple times
        print(get_all_schemas())


if __name__ == "__main__":
    # Call the test bench function
    test_bench()




