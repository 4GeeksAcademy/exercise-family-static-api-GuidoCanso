"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = jsonify(members)
    return response_body, 200

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_members_id(member_id):
    members = jackson_family.get_member(member_id)
    if members is None:
        return jsonify({"msg": "Member not found"}), 404
    response_body = {
        "id": members["id"],
        "first_name": members["first_name"],
        "last_name": members["last_name"],
        "age": members["age"],
        "lucky_numbers": members["lucky_numbers"]
    }
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def handle_post_members():
    member = request.json
    jackson_family.add_member(member)
    new_member = jackson_family.get_member(member["id"])
    return jsonify(new_member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_members(member_id):
    members = jackson_family.delete_member(member_id)
    if members is None:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
