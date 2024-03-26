**User Table:**

This table is used to store information about users of a system. Each row represents a user, with details such as their name, username, password, and whether they have administrative privileges (`is_admin`).

- Schema:
  - user_id: INTEGER (Primary Key)
  - first_name: TEXT
  - last_name: TEXT
  - username: TEXT (Unique)
  - password: TEXT
  - is_admin: BOOLEAN

- SQL Code:

  ```sql
  CREATE TABLE User (
      user_id INTEGER PRIMARY KEY,
      first_name TEXT,
      last_name TEXT,
      username TEXT UNIQUE,
      password TEXT,
      is_admin BOOLEAN
  );
  ```

**missingPerson Table:**

This table is designed to store information about missing persons. Each row represents a missing person, with details such as their name, image (perhaps a photo of the missing person), current status, last known location, time of disappearance, whether they are flagged to be tracked, and the time when the information was uploaded.

- Schema:
  - id: INTEGER (Primary Key, Autoincrement)
  - name: VARCHAR(255)
  - image: BLOB
  - status: BOOLEAN
  - location: VARCHAR(255)
  - time: DATETIME
  - to_be_tracked: BOOLEAN
  - uploadtime: DATETIME

- SQL Code:
  ```sql
  CREATE TABLE missingPerson (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(255),
      image BLOB,
      status BOOLEAN,
      location VARCHAR(255),
      time DATETIME,
      to_be_tracked BOOLEAN,
      uploadtime DATETIME
  );
  ```