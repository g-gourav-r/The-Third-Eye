from flask import render_template, request, redirect, url_for
import sqlite3
from surveillance_system.database import connect_database, save_missing_person, update_missing_person_status, get_missing_persons

def upload_picture():
    """
    Handles uploading a picture of a missing person.
    """
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['file']

        if name and file:
            last_row_id = save_missing_person(name, file)
            if last_row_id:
                return render_template('add_person.html', show_success=True, entry_id=last_row_id)
            else:
                return render_template('add_person.html', show_success=False, error='An error occurred while saving the person.')
        else:
            return render_template('add_person.html', show_success=False, error='Name and file are required.')

    return render_template('add_person.html', show_success=False)

def admin_dashboard():
    """
    Renders the admin dashboard page with information about missing persons.
    """
    missing_persons = get_missing_persons()
    return render_template('admin_dashboard.html', missing_persons=missing_persons)

def user_dashboard():
    """
    Renders the user dashboard
    """
    missing_persons = get_missing_persons()
    return render_template('user_dashboard.html', data=missing_persons)

def logs():
    """
    Renders the logs page with information about missing persons.
    """
    missing_persons = get_missing_persons()
    return render_template('logs.html', data=missing_persons)

def update_status(id, status, location=None, location_image=None):
    """
    Updates the status and location of a missing person.
    """
    if update_missing_person_status(id, status, location, location_image):
        return True
    else:
        return False

def delete_person(id):
    """
    Deletes a missing person from the system.
    """
    conn = connect_database()
    try:
        with conn:
            conn.execute("DELETE FROM missingPerson WHERE id = ?", (id,))
    except Exception as e:
        print(f"An error occurred while deleting user: {e}")
    finally:
        conn.close()

    return redirect(url_for('logs'))