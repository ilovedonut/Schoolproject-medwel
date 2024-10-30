
import function as fn
cursor = fn.cursor

cursor.execute("CREATE DATABASE IF NOT EXISTS user_ids")
cursor.execute("USE user_ids")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'patient',
                    password VARCHAR(255) NOT NULL,
                    first INT(20) DEFAULT 1,
                    area VARCHAR(20) NOT NULL,
                    email VARCHAR(100) ,
                    notifs INT DEFAULT 1
         )
               
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical (
               id INT references users.id ,
               med_data varchar(100) ,
               doctors varchar(50) ,
               feedback varchar(50)
                     
         )
               
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT,
        sender_id INT,
        recipient_id INT,
        message_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    )
""")  