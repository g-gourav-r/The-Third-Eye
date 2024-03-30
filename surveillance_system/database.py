import sqlite3
from datetime import datetime
import hashlib
import os
import base64

upload_folder = "./database/missing_person"


def connect_database():
    """
    Connects to the SQLite database.
    """
    return sqlite3.connect('./database/database.db')

def initialize_database():
    """
    Initializes the database schema if not already created.
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        is_admin INTEGER NOT NULL DEFAULT 0
                    )''')

    # Create missing person table
    cursor.execute('''CREATE TABLE IF NOT EXISTS missingPerson (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        image BLOB NOT NULL,
                        status INTEGER NOT NULL DEFAULT 0,
                        location TEXT,
                        location_image BLOB,
                        time TEXT,
                        to_be_tracked INTEGER NOT NULL DEFAULT 1,
                        uploadtime TEXT NOT NULL DEFAULT CURRENT_TIME
                    )''')
    
    # Add a super admin
    hashed_password = hashlib.sha256("admin@1234".encode('utf-8')).hexdigest()
    cursor.execute("INSERT INTO User (first_name, last_name, username, password, is_admin) VALUES ('Super', 'Admin', 'admin', ?, 1);", (hashed_password,))

    conn.commit()
    conn.close()

def save_user(first_name, last_name, username, password, is_admin=0):
    """
    Saves a new user to the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        cursor.execute('INSERT INTO User (first_name, last_name, username, password, is_admin) VALUES (?, ?, ?, ?, ?)',
                       (first_name, last_name, username, hashed_password, is_admin))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error saving user: {e}")
        return False
    finally:
        conn.close()

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

def save_missing_person(name, file):
    """
    Saves a new missing person to the database and in a folder.
    """
    conn = connect_database()
    cursor = conn.cursor()
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    temp_file_path = os.path.join(upload_folder, 'temp.jpg')
    file.save(temp_file_path)
    with open(temp_file_path, 'rb') as temp_file:
        image_data = temp_file.read()
    os.remove(temp_file_path)
    cursor.execute('INSERT INTO missingPerson (name, image) VALUES (?, ?)', (name, image_data))
    conn.commit()
    cursor.execute('SELECT last_insert_rowid()')
    last_row_id = cursor.fetchone()[0]
    new_file_name = f"{name}_{last_row_id}.jpg"
    file_path = os.path.join(upload_folder, new_file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(image_data)
    conn.close()

    return last_row_id


def update_missing_person_status(id, status, location=None, location_image=None):
    """
    Updates the status and location of a missing person in the database.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        now = datetime.now()
        time_str = now.strftime('%d-%B-%Y %I:%M:%S %p')
        cursor.execute('UPDATE missingPerson SET status = ?, location = ?, location_image = ?, time = ? WHERE id = ?',
                       (status, location, location_image, time_str, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating missing person status: {e}")
        return False
    finally:
        conn.close()

def get_missing_persons():
    """
    Retrieves information about missing persons from the database.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM missingPerson')
        missing_persons = cursor.fetchall()
        decoded_targets = []
        for target in missing_persons:
            target_id, name, image, status, location, time, to_be_tracked, uploadtime = target
            try:
                decoded_image = base64.b64encode(image).decode('utf-8')
            except Exception as e:
                print(f"Error decoding image: {e}")
                decoded_image = None
            decoded_targets.append({
                'target_id': target_id,
                'name': name,
                'decoded_image': decoded_image,
                'status': status,
                'last location': location,
                'time': time,
                'to_be_tracked': to_be_tracked,
                'uploadTime': uploadtime
            })
        return decoded_targets
    except sqlite3.Error as e:
        print(f"Error retrieving missing persons: {e}")
        return None
    finally:
        conn.close()

