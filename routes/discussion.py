from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

bp = Blueprint('discussion', __name__, url_prefix='/')




@bp.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT a.id, a.name,
               COUNT(DISTINCT t.id) AS thread_count,
               COUNT(m.id) AS message_count
        FROM areas a
        LEFT JOIN threads t ON a.id = t.area_id
        LEFT JOIN messages m ON t.id = m.thread_id
        GROUP BY a.id
        ORDER BY a.name;
    ''')

    areas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', areas=areas)





@bp.route('/<int:area_id>/threads')
def view_threads(area_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT t.id, t.title, MAX(m.created_at) AS last_message
        FROM threads t
        LEFT JOIN messages m ON t.id = m.thread_id
        WHERE t.area_id = %s
        GROUP BY t.id
        ORDER BY last_message DESC;
    ''', (area_id,))

    threads = cur.fetchall()
    if not threads:
        flash('Thread not found.', 'error')

    cur.close()
    conn.close()
    return render_template('threads.html', threads=threads, area_id=area_id)

@bp.route('/<int:area_id>/new_thread', methods=['GET', 'POST'])
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
        except Exception as e:
            conn.rollback()
            flash(f'Error creating thread: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('discussion.view_threads', area_id=area_id))
    return render_template('new_thread.html', area_id=area_id)


@bp.route('/area/thread/<int:thread_id>/new_message', methods=['POST'])
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

    return redirect(url_for('discussion.view_messages', thread_id=thread_id))


@bp.route('/area/thread/<int:thread_id>')
def view_messages(thread_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT title FROM threads WHERE id = %s;
    ''', (thread_id,))
    thread = cur.fetchone()
    if not thread:
        flash('Thread not found.', 'error')
        return redirect(url_for('discussion.index'))

    cur.execute('''
        SELECT m.content, u.username, m.created_at, u.id AS user_id
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.thread_id = %s
        ORDER BY m.created_at ASC;
    ''', (thread_id,))
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template(
        'messages.html', 
        messages=messages, 
        thread_id=thread_id, 
        thread_title=thread[0])


