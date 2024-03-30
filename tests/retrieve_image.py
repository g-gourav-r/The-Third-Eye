import sqlite3
import os

def connect_database():
    """
    Connects to the SQLite database.
    """
    return sqlite3.connect('../database/database.db')

def retrieve_image(person_id, output_folder):
    """
    Retrieves the image data for a given missing person ID from the database and saves it to a file.
    """
    conn = connect_database()
    cursor = conn.cursor()

    try:
        # Retrieve the image data for the given person_id
        cursor.execute('SELECT image FROM missingPerson WHERE id = ?', (person_id,))
        image_data = cursor.fetchone()[0]

        # Construct the file path to save the image
        file_path = os.path.join(output_folder, f"missing_person_{person_id}.jpg")

        # Save the image data to a file
        with open(file_path, 'wb') as file:
            file.write(image_data)

        print(f"Image for missing person ID {person_id} saved to: {file_path}")
    except sqlite3.Error as e:
        print(f"Error retrieving image: {e}")
    finally:
        conn.close()

# Example usage
retrieve_image(34, "output_folder")
