from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_del_producto = db.Column(db.String(255), nullable=False)
    descripcion_del_producto = db.Column(db.Text)
    preguntas = db.relationship('Pregunta', backref='producto', lazy='dynamic')

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(1024), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    padre_id = db.Column(db.Integer, db.ForeignKey('pregunta.id', ondelete='CASCADE'))
    preguntas_hijas = db.relationship('Pregunta', backref=db.backref('padre', remote_side=[id]), lazy='dynamic')

class Opcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    respuesta_breve = db.Column(db.String(1024), nullable=True)