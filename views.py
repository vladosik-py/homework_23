from flask import Flask, Blueprint, request, jsonify
from marshmallow import ValidationError

from converter import convert_query
from models import BatchRequestSchema

main_bp = Blueprint('main', __name__)

FILE_NAME = 'data/apache_logs.txt'


@main_bp.route('/perform_query', methods=['POST'])
def perform_query():
    data = request.json

    try:
        validated_data = BatchRequestSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    result = None
    for query in validated_data['queries']:
        result = convert_query(
            cmd=query['cmd'],
            value=query['value'],
            file_name=validated_data['file_name'],
            data=result,
        )

        return jsonify(result)
