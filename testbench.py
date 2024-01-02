from utils import *

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
        print(get_schema(id=str(schema_id)))

        # Adding data multiple times for different schemas
        schema_id = myschemas.find_one({"name": "Schema1"})["_id"]
        data_string = {"name": "Alice"}
        print(add_data(str(schema_id), data_string))

        schema_id = myschemas.find_one({"name": "Schema2"})["_id"]
        data_integer = {"salary": 50000.00, "active": True}
        print(add_data(str(schema_id), data_integer))

        # Retrieving data of schemas multiple times
        schema_id1 = myschemas.find_one({"name": "Schema1"})["_id"]
        schema_id2 = myschemas.find_one({"name": "Schema2"})["_id"]
        print(get_data_of_schema(id=str(schema_id1)))
        print(get_data_of_schema(id=str(schema_id2)))

        # Retrieving all schemas multiple times
        print(get_all_schemas())


def test_more():
    print(get_schema(name="Schema1"))
    schema_id = myschemas.find_one({"name": "Schema2"})["_id"]
    print(schema_id)
    print(get_schema(id=ObjectId("65945eb9140793ac92c1f819")))

if __name__ == "__main__":
    # Call the test bench function
    test_bench()
    test_more()