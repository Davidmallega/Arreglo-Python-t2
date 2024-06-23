from flask import Flask
from config import Config
from models import init_app
from routes.index import index_bp
from routes.agregar import agregar_bp
from routes.mostrar import mostrar_bp
from routes.actualizar import actualizar_bp
from routes.eliminar import eliminar_bp
from routes.generar_pdf import generar_pdf_bp

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  # Mensajes para Flask

# Inicializar la base de datos
init_app(app)

# Registrar blueprints
app.register_blueprint(index_bp)
app.register_blueprint(agregar_bp)
app.register_blueprint(mostrar_bp)
app.register_blueprint(actualizar_bp)
app.register_blueprint(eliminar_bp)
app.register_blueprint(generar_pdf_bp)

if __name__ == '__main__':
    app.run(debug=True)

