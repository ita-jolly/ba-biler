import os
from flask import Flask, request, jsonify, make_response
import db_service
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
from swagger.config import swagger_config

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)

db_service.init()


@app.route('/')
def index():
  return "Welcome to API"

@app.route('/biler', methods=['GET'])
@swag_from('swagger/get_biler.yml')
def get_biler():
    biler = db_service.get_biler()

    if biler is None:
        response = make_response({'message': 'Ingen biler fundet'}, 404)
    else:
        response = make_response(biler, 200)

    return response

@app.route('/biler/udlejet', methods=['GET'])
@swag_from('swagger/get_udlejet.yml')
def get_udlejet():
    biler = db_service.get_udlejede_biler()

    if biler is None:
        response = make_response({'message': 'Ingen biler er udlejet.'}, 404)
    else:
        response = make_response(biler, 200)

    return response

@app.route('/biler/<string:nummerplade>', methods=['PATCH'])
def update_bil_status(nummerplade):
    try:
        # Parse the incoming JSON
        data = request.get_json()

        # Check if 'udlejnings_status' is present
        if 'udlejnings_status' not in data:
            return jsonify({"error": "Missing 'udlejnings_status' field"}), 400

        # Update the status using db_service
        updated = db_service.update_udlejnings_status(
            nummerplade=nummerplade,
            status=data['udlejnings_status']
        )

        # Handle different outcomes
        if updated is None:
            return jsonify({"error": f"Nummerplade {nummerplade} not found in biler database"}), 404
        elif not updated:
            return jsonify({"error": "Failed to update the record due to a database error."}), 500

        return jsonify({"message": f"Udlejnings_status for nummerplade {nummerplade} updated to {data['udlejnings_status']}."}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# @app.route('/gettemplate', methods=['GET'])
# @swag_from('swagger/get_template.yml')

if __name__ == '__main__':
    app.run(port=5000)
