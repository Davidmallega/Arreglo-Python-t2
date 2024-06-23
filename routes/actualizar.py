from flask import Blueprint, render_template, request, redirect, url_for
from models import mysql
from babel.numbers import format_currency

actualizar_bp = Blueprint('actualizar', __name__)

@actualizar_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        talla = request.form['talla']
        color = request.form['color']
        material = request.form['material']
        unidades = request.form['unidades']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET marca=%s, modelo=%s, talla=%s, color=%s, material=%s, unidades=%s, precio=%s
            WHERE id=%s
        """, (marca, modelo, talla, color, material, unidades, precio, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mostrar.mostrar'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cur.fetchone()
    cur.close()
    
    # Formatear el precio a CLP
    if producto:
        producto = list(producto)
        producto[7] = format_currency(producto[7], 'CLP', locale='es_CL')
    
    return render_template('actualizar.html', producto=producto)
