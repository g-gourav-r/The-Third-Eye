import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os
import sqlite3

def generate_frames():
    """
    Generates frames from the camera feed and performs face recognition.
    """
    video_capture = cv2.VideoCapture(0) 

    path = './database/missing_person'
    images = []
    classNames = []
    mylist = os.listdir(path)

    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    encoded_face_train = find_encodings(images)

    while True:
        success, frame = video_capture.read()
        if not success:
            break 
        else:
            imgS = cv2.resize(frame, (0,0), None, 0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faces_in_frame = face_recognition.face_locations(imgS)
            encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
            for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
                matches = face_recognition.compare_faces(encoded_face_train, encode_face)
                faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
                matchIndex = np.argmin(faceDist)
                name = "Unknown"
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper().lower()
                    name = name.title()
                    person_name = name.split('_')[0]
                    y1,x2,y2,x1 = faceloc
                    y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(frame, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
                    cv2.putText(frame,person_name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    print(name)
                    find_person(name)
                    update_db(name)
                else:
                    # If no match found, you can handle it here
                    pass
                    
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def find_encodings(images):
    """
    Finds encodings for the faces in the given images.
    """
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

def find_person(name):
    """
    Finds a person in the system and logs the detection.
    """
    with open('./database/all_logs.csv', 'a+') as f:
        f.seek(0)  # Move the file pointer to the beginning to read existing data
        myDataList = f.readlines()
        nameList = [entry.split(',')[0].strip() for entry in myDataList]
        
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S %p')
            date = now.strftime('%d-%B-%Y')
            location = "Camera 1"
            entry = f"{name.split('_')[1]}, {name.split('_')[0]}, {time}, {date}, {location}\n"
            f.write(entry)
 
def update_db(name):
    """
    Updates the database with the detection information.
    """
    base_name = name.split('.')[0]
    number_part = base_name.split('_')[1]
    number = int(number_part)
    now = datetime.now()
    time_str = now.strftime('%I:%M:%S %p')
    date_str = now.strftime('%d-%B-%Y')
    time = f'{date_str} {time_str}'
    conn = sqlite3.connect('./database/database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE missingPerson SET status = 1, location = "Camera 1", time = ? WHERE id = ?', (time, number))
        conn.commit()
        print(f"Record with id {number} updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
