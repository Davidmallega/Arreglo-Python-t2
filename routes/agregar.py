from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import mysql

agregar_bp = Blueprint('agregar', __name__)

@agregar_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        talla = request.form['talla']
        color = request.form['color']
        material = request.form['material']
        unidades = request.form['unidades']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (marca, modelo, talla, color, material, unidades, precio) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (marca, modelo, talla, color, material, unidades, precio))
        mysql.connection.commit()
        cur.close()
        flash('Producto guardado con éxito!', 'success')
        return redirect(url_for('index.index'))
    return render_template('agregar.html')
