from flask import Flask, render_template, redirect, url_for, request, session, flash
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


@app.route('/')
def base():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM areas;')
    areas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('base.html', areas=areas)

@app.route('/discussion')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM areas;')
    areas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', areas=areas)



@app.route('/area/<int:area_id>/threads')
def view_threads(area_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM threads WHERE area_id = %s;', (area_id,))
    threads = cur.fetchall()
   # print(f'Threads for area {area_id}: {threads}') #debug
    if not threads:
        flash('Thread not found.', 'error')
        #return redirect(url_for('index'))
    cur.close()
    conn.close()
    return render_template('threads.html', threads=threads, area_id=area_id)


@app.route('/area/<int:area_id>/new_thread', methods=['GET', 'POST'])
def new_thread(area_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO threads (title, area_id) VALUES (%s, %s) RETURNING id;', (title, area_id))
            thread_id = cur.fetchone()[0]

            cur.execute(
                'INSERT INTO messages (content, thread_id, user_id) VALUES (%s, %s, %s);',
                (content, thread_id, session.get('user_id'))
            )
            conn.commit()
            flash('New thread created successfully!', 'success')
        except psycopg2.Error as e:
            conn.rollback()
            flash(f'Error creating thread: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('view_threads', area_id=area_id))

    return render_template('new_thread.html', area_id=area_id)


@app.route('/thread/<int:thread_id>/new_message', methods=['POST'])
def new_message(thread_id):
    if 'user_id' not in session:
        flash('You must be logged in to post a message.', 'error')
        return redirect('/login')

    content = request.form['content']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO messages (content, thread_id, user_id, created_at)
            VALUES (%s, %s, %s, NOW());
        ''', (content, thread_id, session['user_id']))
        conn.commit()
        flash('Message posted successfully.')
    except psycopg2.Error as e:
        conn.rollback()
        flash(f'Error posting message: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('view_messages', thread_id=thread_id))


@app.route('/thread/<int:thread_id>')
def view_messages(thread_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT title FROM threads WHERE id = %s;
    ''', (thread_id,))
    thread = cur.fetchone()
    if not thread:
        flash('Thread not found.', 'error')
        return redirect(url_for('index'))

    cur.execute('''
        SELECT m.content, u.username, m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.thread_id = %s;
    ''', (thread_id,))
    messages = cur.fetchall()
    cur.close()
    conn.close()
#    return render_template('messages.html', messages=messages, thread_id=thread_id)
    return render_template('messages.html', messages=messages, thread_id=thread_id, thread_title=thread[0])


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, password)
            )
            conn.commit()
            flash('User added successfully!', 'success')
        except psycopg2.Error as e:
            conn.rollback()
            flash(f'Error adding user: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template('add_user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT id, username, password FROM users WHERE username = %s',
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('You are now logged in', 'success')
            return redirect(url_for('base'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('base'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    return 'Registration page coming soon.'


if __name__ == '__main__':
    app.run(debug=True)

