import logging
from dotenv import load_dotenv
from flask import Flask, jsonify

from src.models.db import init_db
from src.errors.errors import ApiError
from src.blueprints.health_blueprint import health_blueprint
from src.blueprints.sesiones_blueprint import sesiones_blueprint


# Configuración logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(name)s: %(message)s')


# Cargar variables de entorno desde el archivo .env
loaded = load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)

# Inicializar base de datos
init_db()

# Registro de blueprints
PREFIJO = '/gestor-sesion-deportiva/'
app.register_blueprint(health_blueprint, url_prefix=PREFIJO+'health')
app.register_blueprint(sesiones_blueprint, url_prefix=PREFIJO+'sesiones')


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "error": err.description
    }
    return jsonify(response), err.code