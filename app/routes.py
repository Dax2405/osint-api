from flask import Blueprint, request, jsonify
from .utils import get_info_by_name as get_info_by_name_util, get_info_by_plate

main = Blueprint('main', __name__)

@main.route('/get_info_by_name', methods=['POST'])
def get_info_by_name_route():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Falta el parámetro 'name'"}), 400
    name = data.get("name")
    result = get_info_by_name_util(name)
    return jsonify(result)
@main.route('/get_info_by_plate', methods=['POST'])
def get_info_by_plate_route():
    plate = request.get_json("plate").get("plate")
    if not plate:
        return jsonify({"error": "Falta el parámetro 'plate'"}), 400
    result = get_info_by_plate(plate)
    return jsonify(result)
