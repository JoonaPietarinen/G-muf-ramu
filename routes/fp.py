from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

bp = Blueprint('fp', __name__, url_prefix='/nan')



@bp.route('/')
def base():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM areas;')
    areas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('base.html', areas=areas)
