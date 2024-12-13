from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:user_id>')
def view_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT u.username, p.bio, p.profile_image,
               COUNT(m.id) AS message_count,
               AVG(LENGTH(m.content)) AS avg_message_length,
               COUNT(DISTINCT t.id) AS active_threads,
               u.created_at
        FROM users u
        LEFT JOIN profiles p ON u.id = p.user_id
        LEFT JOIN messages m ON u.id = m.user_id
        LEFT JOIN threads t ON m.thread_id = t.id
        WHERE u.id = %s
        GROUP BY u.id, p.bio, p.profile_image;
    ''', (user_id,))
    profile = cur.fetchone()
    cur.close()
    conn.close()

    if profile:
        return render_template('profile.html', profile=profile, user_id=user_id)
    else:
        flash('User not found.', 'error')
        return redirect('/')



@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Unauthorized access.', 'error')
        return redirect('/')

    if request.method == 'POST':
        bio = request.form['bio']
        profile_image = request.form['profile_image']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO profiles (user_id, bio, profile_image)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET bio = EXCLUDED.bio, profile_image = EXCLUDED.profile_image;
            ''', (user_id, bio, profile_image))
            conn.commit()
            flash('Profile updated successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('profile.view_profile', user_id=user_id))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT bio, profile_image FROM profiles WHERE user_id = %s;', (user_id,))
    profile = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit_profile.html', profile=profile)
