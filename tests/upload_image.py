import sqlite3

def upload_image_to_database(image_path):
    try:
        # Connect to the SQLite3 database
        conn = sqlite3.connect('image_database.db')
        cursor = conn.cursor()

        # Read the image file as binary data
        with open(image_path, 'rb') as file:
            image_data = file.read()

        # Execute an SQL INSERT statement to store the image data in the database
        cursor.execute('INSERT INTO images (image_data) VALUES (?)', (sqlite3.Binary(image_data),))
        
        # Commit the transaction to save the changes
        conn.commit()
        
        print("Image uploaded successfully.")

    except sqlite3.Error as e:
        print(f"Error uploading image to database: {e}")

    finally:
        # Close the database connection
        conn.close()

# Example usage
image_path = './output_folder/test.jpg'
upload_image_to_database(image_path)
