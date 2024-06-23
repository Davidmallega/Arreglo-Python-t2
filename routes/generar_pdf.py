from flask import Blueprint, send_file
from models import mysql
from babel.numbers import format_currency
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

generar_pdf_bp = Blueprint('generar_pdf', __name__)

@generar_pdf_bp.route('/generar_pdf')
def generar_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()

    # Datos de la tabla
    data = [['ID', 'Marca', 'Modelo', 'Talla', 'Color', 'Material', 'Unidades', 'Precio']]
    total_precio = 0
    for producto in productos:
        producto_formateado = list(producto)
        precio = producto_formateado[7]
        total_precio += precio
        precio_formateado = format_currency(precio, 'CLP', locale='es_CL')
        data.append([producto_formateado[0], producto_formateado[1], producto_formateado[2], producto_formateado[3], producto_formateado[4], producto_formateado[5], producto_formateado[6], precio_formateado])
    
    total_precio_formateado = format_currency(total_precio, 'CLP', locale='es_CL')

    # Estilos de la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Título
    title = "Lista de Productos Inventariados"
    title_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ])

    # Crear la tabla del título
    title_table = Table([[title]], colWidths=[500])
    title_table.setStyle(title_style)

    # Agregar título, tabla y total al documento
    elements.append(title_table)
    elements.append(table)
    elements.append(Table([['', '', '', '', '', '', 'Total', total_precio_formateado]], colWidths=[50, 50, 50, 50, 50, 50, 50, 100]))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='informe_productos.pdf', mimetype='application/pdf')

