from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # Importa Flask-CORS
from api.con_frontend.HelloApiHandler import HelloApiHandler
from api.con_frontend.ParametersApiHandler import ParametersApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app, supports_credentials=True)  # Habilita el soporte de credenciales
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

# Ruta para servir la imagen
@app.route('/horario.png')
def serve_image():
    return send_from_directory('api/resources', 'horario.png')

api.add_resource(HelloApiHandler, '/flask/hello')
api.add_resource(ParametersApiHandler, '/genhor/parameter')
