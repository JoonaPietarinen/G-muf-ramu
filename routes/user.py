from flask import Blueprint, render_template, request, redirect, flash
from database import get_db_connection

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s);', (username, password))
            conn.commit()
            flash('User added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error adding user: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return redirect('/login')
    return render_template('add_user.html')
