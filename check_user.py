import sqlite3

conn = sqlite3.connect("file_sharing.db")
cursor = conn.cursor()

cursor.execute("SELECT email, password FROM users WHERE email = ?", ("namratasinghsanjana@gmail.com",))
user = cursor.fetchone()

if user:
    print("Email:", user[0])
    print("Stored hash:", user[1])
else:
    print("User not found.")

conn.close()
