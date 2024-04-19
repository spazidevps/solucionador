from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Asegúrate de que esto esté configurado correctamente
app.secret_key = '12345abcde67890fghij12345'  # Cambia esto por algo más seguro

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/solu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Asegúrate de que los imports de tus vistas se hagan después de configurar la clave secreta
from .views import views
