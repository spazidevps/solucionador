from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models.models import Producto, Pregunta, Opcion

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        nuevo_producto = Producto(nombre_del_producto=nombre, descripcion_del_producto=descripcion)
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado con éxito!')
        return redirect(url_for('crear_producto'))
    return render_template('crear_producto.html')

@app.route('/ver_productos')
def ver_productos():
    productos = Producto.query.all()
    return render_template('ver_productos.html', productos=productos)


@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre_del_producto = request.form['nombre']
        producto.descripcion_del_producto = request.form['descripcion']
        db.session.commit()
        flash('Producto actualizado con éxito!')
        return redirect(url_for('ver_productos'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito!')
    return redirect(url_for('ver_productos'))

@app.route('/ver_producto/<int:id>')
def ver_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('perfil_producto.html', producto=producto)

@app.route('/crear_solucion/<int:producto_id>', methods=['GET', 'POST'])
def crear_solucion(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if request.method == 'POST':
        main_question_text = request.form.get('pregunta')
        if main_question_text:
            main_question = Pregunta(texto=main_question_text, producto_id=producto_id)
            db.session.add(main_question)
            db.session.flush()

        # Procesar todas las opciones y subpreguntas
        for key, values in request.form.lists():
            if key.startswith('options['):
                # Asegurar que el ID es numérico
                raw_id = key.split('[')[1].split(']')[0]
                if raw_id.isdigit():
                    question_id = int(raw_id)
                    for value in values:
                        new_option = Opcion(texto=value, pregunta_id=question_id)
                        db.session.add(new_option)
            elif key.startswith('brief['):
                option_id = key.split('[')[1].split(']')[0]
                if option_id.isdigit():
                    for value in values:
                        option = Opcion.query.get(int(option_id))
                        if option:
                            option.respuesta_breve = value
                            db.session.add(option)

        db.session.commit()
        flash('Solución creada con éxito!')
        return redirect(url_for('ver_producto', id=producto_id))

    return render_template('crear_solucion.html', producto=producto)