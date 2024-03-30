from flask import render_template, redirect, url_for, request
import hashlib
import sqlite3
from surveillance_system.database import connect_database, save_user


def login():
    """
    Handles user login functionality.
    """
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user = get_user(username)
        if user is None:
            error = 'User does not exist.'
        elif user[4] == hashed_password:
            if user[5] == 0:
                # Redirect to user dashboard
                return redirect(url_for('user_dashboard'))
            else:
                # Redirect to admin dashboard
                return redirect(url_for('admin_dashboard'))
        else:
            error = 'Wrong Password'

    return render_template('login.html', error=error)

def add_user():
    """
    Handles adding a new user to the system.
    """
    error = None
    status = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        is_admin = 1 if 'is_admin' in request.form else 0

        if len(password) < 6:
            error = 'Password should be at least 6 characters long.'
        elif password != request.form['confirm_password']:
            error = 'Passwords do not match.'
        elif save_user(first_name, last_name, username, password, is_admin):
            status = f'{username} added as {"User" if is_admin == 0 else "Admin"}'
        else:
            error = 'An error occurred. Please try again.'

    return render_template('add_user.html', error=error, status=status)

def manage_user():
    """
    Renders the user management page with a list of users.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM User')
        users = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        users = []
    conn.close()
    return render_template('manage_user.html', users=users)

def toggle_admin(user_id):
    """
    Toggles the admin status of a user.
    """
    is_admin = int(request.form['is_admin'])
    conn = connect_database()
    try:
        with conn:
            conn.execute("UPDATE User SET is_admin = ? WHERE user_id = ?", (is_admin, user_id))
    except Exception as e:
        print(f"An error occurred while updating is_admin: {e}")
    finally:
        conn.close()
    return redirect(url_for('manage_user'))

def delete_user(user_id):
    """
    Deletes a user from the system.
    """
    conn = connect_database()
    try:
        with conn:
            conn.execute("DELETE FROM User WHERE user_id = ?", (user_id,))
    except Exception as e:
        print(f"An error occurred while deleting user: {e}")
    finally:
        conn.close()

    return redirect(url_for('manage_user'))

def get_user(username):
    """
    Retrieves user information from the database by username.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM User WHERE username=?', (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        conn.close()