from flask import Blueprint, redirect, url_for
from models import mysql

eliminar_bp = Blueprint('eliminar', __name__)

@eliminar_bp.route('/eliminar/<int:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('mostrar.mostrar'))
