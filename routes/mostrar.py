from flask import Blueprint, render_template, request
from models import mysql
from babel.numbers import format_currency

mostrar_bp = Blueprint('mostrar', __name__)

@mostrar_bp.route('/mostrar')
def mostrar():
    marca_filtro = request.args.get('marca')
    cur = mysql.connection.cursor()
    
    # Obtener todas las marcas
    cur.execute("SELECT DISTINCT marca FROM productos")
    marcas = [row[0] for row in cur.fetchall()]
    
    if marca_filtro:
        cur.execute("SELECT * FROM productos WHERE marca = %s", (marca_filtro,))
    else:
        cur.execute("SELECT * FROM productos")
    
    productos = cur.fetchall()
    cur.close()
    
    # Formatear el precio y calcular el total
    total_precio = 0
    productos_formateados = []
    for producto in productos:
        producto_formateado = list(producto)
        precio = producto_formateado[7]
        total_precio += precio
        producto_formateado[7] = format_currency(precio, 'CLP', locale='es_CL')
        productos_formateados.append(producto_formateado)
    
    total_precio_formateado = format_currency(total_precio, 'CLP', locale='es_CL')
    
    return render_template('mostrar.html', productos=productos_formateados, total_precio=total_precio_formateado, marcas=marcas, marca_seleccionada=marca_filtro)

