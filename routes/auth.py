from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, username, password FROM users WHERE username = %s;', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('fp.base'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('fp.base'))
