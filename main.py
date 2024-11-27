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


# @app.route('/gettemplate', methods=['GET'])
# @swag_from('swagger/get_template.yml')

if __name__ == '__main__':
    app.run()
