import json

from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


# API endpoints
@app.route('/insert-schema', methods=['POST'])
def insert_schema_route():
    request_data = request.json
    result = insert_schema(request_data.get("schema"), request_data.get("name"), request_data.get("description"))
    return {"status": result}


@app.route('/get-schema', methods=['GET'])
def get_schema_route():
    schema_id = request.args.get('id')
    schema_name = request.args.get('name')
    result = get_schema(id=schema_id, name=schema_name)
    return str(result)


@app.route('/add-data/<schema_id>', methods=['POST'])
def add_data_route(schema_id):
    request_data = request.json

    result = add_data(schema_id, request_data)
    return {"status": result}


@app.route('/get-all-schemas', methods=['GET'])
def get_all_schemas_route():
    all_schemas = get_all_schemas()
    resultDict = {"all_schemas": str(all_schemas)}
    return resultDict

@app.route('/get-schema-data', methods=['GET'])
def get_schema_data_route():
    schema_id = request.args.get('id')
    schema_name = request.args.get('name')
    result = get_data_of_schema(id=schema_id, name=schema_name)
    resultDict = {"data": str(result)}
    return resultDict


if __name__ == '__main__':
    app.run(port=8000, debug=True)
